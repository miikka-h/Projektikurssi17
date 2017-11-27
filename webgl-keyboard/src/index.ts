

import {Renderer} from "./renderer";

main();

function main() {
    const canvas = document.getElementById("glCanvas") as HTMLCanvasElement;

    const gl = canvas.getContext("webgl");

    if (gl === null) {
        console.error("webgl not supported");
        return;
    }

    const renderer = Renderer.create(gl);

    if (renderer === null) {
        return;
    }

    renderer.draw();
}
