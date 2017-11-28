import { Cube } from "./cube";
import { Triangle } from "./triangle";
import { mat4, vec3 } from "gl-matrix";

export class Keyboard {
    public cube: Cube;
    public triangle: Triangle;

    public keyboardCase: Cube;

    constructor() {
        this.cube = new Cube();
        mat4.fromTranslation(this.cube.modelMatrix, [2,0,-10]);

        this.triangle = new Triangle();
        mat4.fromTranslation(this.triangle.modelMatrix, [0,0,-10])

        this.keyboardCase = new Cube();
        mat4.fromScaling(this.keyboardCase.modelMatrix, [4, 0.30, 2]);

    }
}