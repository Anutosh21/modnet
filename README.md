# Let's change our camera's background in a notebook

Try the included portrait or turn on your camera. Remove the background, blur it,
change its colour, or view the foreground mask. Your photos and camera frames stay
in this browser.

- [Open the WebGPU notebook](https://anutosh21.github.io/modnet/lab/index.html?path=live-camera-webgpu.ipynb)
- [Open the CPU notebook](https://anutosh21.github.io/modnet/lab/index.html?path=live-camera-cpu.ipynb)
- [Open the optional benchmark](https://anutosh21.github.io/modnet/lab/index.html?path=benchmark.ipynb)

Both notebooks include completed outputs and a sample before/after image. To try
the live demo, select **Run → Run All Cells** in a fresh kernel, then click
**Start camera** and allow access. You can also use the sample portrait or upload
a photo. Run one notebook at a time when comparing CPU and WebGPU.

PyTorch, compilation and model execution run in your browser. The model code
and sample portrait are included in `content/`.

The original 25 MiB checkpoint is included in `content/`, so the model-loading
cell reads it directly from the kernel filesystem. The browser caches the site
assets. A download fallback remains available for deployments without the file.

The main notebooks take you straight to the live preview. Optional eager-reference
checks and CPU/WebGPU measurements are in `content/benchmark.ipynb`; a recorded
comparison is in `content/benchmark-results.json`. Run the benchmark separately
when needed. Its completed outputs show the recorded timings; each new run also
saves a device-specific JSON report.

Shoutout to [MODNet](https://github.com/ZHKKKe/MODNet) and the
[ExecuTorch background-removal demo](https://executorch.ai/playground/webgpu/#/demo/bgremove)
for the inspiration! Built from the
[Xeus-Lite template](https://github.com/jupyterlite/xeus-lite-demo).

The portrait shows Eileen Collins: NASA, public domain. Model licensing and source
details are in `content/LICENSE-MODNet` and `content/sources.json`.

To deploy, set **Settings → Pages → Source → GitHub Actions**, then push to `main`.

The browser bundle omits development headers, static libraries and package tests.
Both notebooks use Turbine/IREE for compilation and execution on their selected device.

To build and check the same site locally before deploying:

```bash
micromamba create -n modnet-site -f .github/build-environment.yml
micromamba run -n modnet-site jupyter lite build --contents content --output-dir dist
micromamba run -n modnet-site python -m http.server 8000 --directory dist
```

Open `http://localhost:8000/lab/index.html` and run either notebook from the top.
