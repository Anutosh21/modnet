# Let's change our camera's background in a notebook

Try the included portrait or turn on your camera. Remove the background, blur it,
change its colour, or view the foreground mask. Your photos and camera frames stay
in this browser.

- [Open the WebGPU notebook](https://anutosh21.github.io/modnet/lab/index.html?path=live-camera-webgpu.ipynb)
- [Open the CPU notebook](https://anutosh21.github.io/modnet/lab/index.html?path=live-camera-cpu.ipynb)

Run the cells from top to bottom in a fresh kernel, then click **Start camera** and
allow access. You can also use the sample portrait or upload a photo. Run one
notebook at a time when comparing CPU and WebGPU.

PyTorch, compilation and model execution run in your browser. The model code,
pretrained weights and sample portrait are included in `content/`.

Shoutout to [MODNet](https://github.com/ZHKKKe/MODNet) and the
[ExecuTorch background-removal demo](https://executorch.ai/playground/webgpu/#/demo/bgremove)
for the inspiration! Built from the
[Xeus-Lite template](https://github.com/jupyterlite/xeus-lite-demo).

The portrait shows Eileen Collins: NASA, public domain. Model licensing and source
details are in `content/LICENSE-MODNet` and `content/sources.json`.

To deploy, set **Settings → Pages → Source → GitHub Actions**, then push to `main`.
