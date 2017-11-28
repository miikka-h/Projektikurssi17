

import {Renderer} from "./renderer";
import { Keyboard } from "./keyboard";

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

    const keyboard = new Keyboard();

    renderer.draw(keyboard);
}
