

import {Renderer} from "./renderer";
import { Keyboard } from "./keyboard";

let renderer: Renderer, keyboard: Keyboard;

main();

function main() {
    const canvas = document.getElementById("glCanvas") as HTMLCanvasElement;

    const gl = canvas.getContext("webgl");

    if (gl === null) {
        console.error("webgl not supported");
        return;
    }

    renderer = Renderer.create(gl);

    if (renderer === null) {
        return;
    }

    keyboard = new Keyboard();

    renderer.draw(keyboard);

    const loadButton = document.getElementById("loadButton");
    loadButton.addEventListener("click", loadHeatmap, false);
}

function loadHeatmap(event: MouseEvent): any {
    if (renderer === null) {
        return;
    }

    let httpRequest = new XMLHttpRequest();

    httpRequest.onreadystatechange = parseHeatmapJSON;
    httpRequest.open("GET", "heatmap.api");
    httpRequest.send();

}

function parseHeatmapJSON(this: XMLHttpRequest, e: Event) {
    if (this.readyState === XMLHttpRequest.DONE) {
        if (this.status === 200) {
            const heatmap = JSON.parse(this.responseText);

            keyboard.updateHeatmap(heatmap);
            renderer.draw(keyboard);

        } else {
            console.error("HTTP GET error");
        }
    }
}