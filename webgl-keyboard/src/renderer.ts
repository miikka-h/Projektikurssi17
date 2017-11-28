
import {glMatrix, mat4, vec3} from "gl-matrix";
import {TriangleRenderer, TriangleProgram} from "./triangle"
import {CubeProgram, CubeRenderer} from "./cube"
import {Keyboard} from "./keyboard";

export class Renderer {
    private projectionMatrix: mat4;
    private viewMatrix: mat4;
    private triangleRenderer: TriangleRenderer;
    private cubeRenderer: CubeRenderer;

    constructor(private gl: WebGLRenderingContext, triangleProgram: TriangleProgram, cubeProgram: CubeProgram) {
        this.projectionMatrix = mat4.create();
        mat4.perspective(this.projectionMatrix, 45 * Math.PI / 180, gl.canvas.width/gl.canvas.height, 0.1, 100);

        this.viewMatrix = mat4.create();
        mat4.lookAt(this.viewMatrix, [5,5,10], [0,0,0], [0,1,0]);

        this.triangleRenderer = new TriangleRenderer(gl, triangleProgram);
        this.cubeRenderer = new CubeRenderer(gl, cubeProgram);

        gl.clearColor(0, 0, 0, 1);
        gl.enable(gl.DEPTH_TEST);
    }

    /**
     * Create WebGL renderer. Returns null if creation failed.
     * @param gl
     */
    static create(gl: WebGLRenderingContext): Renderer {
        const triangleProgram = TriangleProgram.create(gl);

        if (triangleProgram === null) {
            return null;
        }

        const cubeProgram = CubeProgram.create(gl);

        if (cubeProgram === null) {
            return null;
        }

        return new Renderer(gl, triangleProgram, cubeProgram);
    }

    draw(keyboard: Keyboard) {
        const gl = this.gl;

        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

        this.cubeRenderer.render(gl, keyboard.cube, this.viewMatrix, this.projectionMatrix);
        this.triangleRenderer.render(gl, keyboard.triangle, this.viewMatrix, this.projectionMatrix);

        this.cubeRenderer.render(gl, keyboard.keyboardCase, this.viewMatrix, this.projectionMatrix);
    }
}