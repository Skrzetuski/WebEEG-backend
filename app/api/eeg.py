import asyncio
import json
import math
from array import array
from typing import Literal

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

router = APIRouter()

@router.websocket("/ws/eeg")
async def eeg_ws(
    ws: WebSocket,
    fmt: Literal["int16-interleaved", "f32-planar"] = Query(default="int16-interleaved"),
    channels: int = Query(default=8, ge=1, le=256),
    sr: int = Query(default=500, ge=1, le=50000),          # sample rate [Hz]
    spf: int = Query(default=20, ge=1, le=100000),         # samples per frame (per channel)
    base_freq: float = Query(default=8.0),                 # częstotliwość 1. kanału [Hz]
    freq_step: float = Query(default=0.5),                 # przyrost f na kanał [Hz]
    amp_i16: int = Query(default=12000, ge=1, le=32767),   # amplituda dla int16
    amp_f32: float = Query(default=40.0),                  # amplituda dla float32
    sleep_comp: float = Query(default=0.0),                # (opcjonalnie) korekta timingu [s]
):
    """
    Strumień EEG – ciągły sinus na każdym kanale:
      f_ch = base_freq + ch * freq_step

    Ramki binarne z ciągłą fazą:
      - int16-interleaved: s[ch0], s[ch1], ..., s[chN-1], s[ch0], ...
      - f32-planar:       [ch0..n-1][ch1..n-1]...

    Przykład połączenia:
      ws://localhost:8000/ws/eeg?fmt=int16-interleaved&channels=8&sr=500&spf=20
    """
    await ws.accept()

    two_pi = 2.0 * math.pi
    omegas = [two_pi * (base_freq + ch * freq_step) / float(sr) for ch in range(channels)]
    phases = [0.0 for _ in range(channels)]

    if fmt == "int16-interleaved":
        frame_arr = array("h", [0] * (channels * spf))
        scale_meta = 1.0 / 32768.0
    else:
        frame_arr = array("f", [0.0] * (channels * spf)) 
        scale_meta = 1.0

    meta = {
        "format": fmt,
        "channels": channels,
        "sampleRate": sr,
        "samplesPerFrame": spf,
        "scale": scale_meta,
        "baseFreq": base_freq,
        "freqStep": freq_step,
    }
    await ws.send_text(json.dumps(meta))

    frame_interval = max(1e-6, spf / float(sr)) - max(0.0, sleep_comp)

    try:
        while True:
            if fmt == "int16-interleaved":
                k = 0
                for i in range(spf):
                    for ch in range(channels):
                        s = math.sin(phases[ch])
                        v = int(amp_i16 * s)
                        frame_arr[k] = v
                        k += 1
                        phases[ch] += omegas[ch]
                        if phases[ch] >= two_pi:
                            phases[ch] -= two_pi
            else: 
                for ch in range(channels):
                    base = ch * spf
                    phi = phases[ch]
                    w = omegas[ch]
                    for i in range(spf):
                        frame_arr[base + i] = amp_f32 * math.sin(phi)
                        phi += w
                        if phi >= two_pi:
                            phi -= two_pi
                    phases[ch] = phi

           
            await ws.send_bytes(frame_arr.tobytes())
            await asyncio.sleep(frame_interval)

    except WebSocketDisconnect:
        return
    except Exception:
        await ws.close(code=1011, reason="server error")
        return
