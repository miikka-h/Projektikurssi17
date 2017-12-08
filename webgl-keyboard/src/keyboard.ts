import { Cube } from "./cube";
import { Triangle } from "./triangle";
import { mat4, vec3 } from "gl-matrix";

const DEFAULT_KEY_SCALE = 0.10;

class Key {
    public cube: Cube;

    constructor(x: number, z: number, xScale: number, zScale: number) {
        this.cube = new Cube();
        mat4.fromScaling(this.cube.modelMatrix, [xScale, DEFAULT_KEY_SCALE, zScale]);
        mat4.translate(this.cube.modelMatrix, this.cube.modelMatrix, [x, 5.0, z]);
    }

    setColor(r: number, b: number, g: number) {
        vec3.set(this.cube.topFaceColor, r, g, b);
    }

    static transformAndScaleX(x: number, z: number, xScale: number): Key {
        return new Key(x, z, xScale, DEFAULT_KEY_SCALE);
    }

    static transform(x: number, z: number): Key {
        return new Key(x, z, DEFAULT_KEY_SCALE, DEFAULT_KEY_SCALE);
    }
}

const END_COLOR = [1.0, 0.0, 0.0];
const START_COLOR = [0.0, 1.0, 0.0];

export class Keyboard {
    public cube: Cube;
    public triangle: Triangle;

    public keyboardCase: Cube;
    public keys: Map<number, Key>;

    constructor() {
        this.cube = new Cube();
        mat4.fromTranslation(this.cube.modelMatrix, [2,0,-10]);

        this.triangle = new Triangle();
        mat4.fromTranslation(this.triangle.modelMatrix, [0,0,-10])

        this.keyboardCase = new Cube();
        mat4.fromScaling(this.keyboardCase.modelMatrix, [4, 0.20, 2]);
        vec3.set(this.keyboardCase.topFaceColor, 0, 0.2, 0.5);

        this.keys = new Map();

        // Id values match Linux kernel input event codes, from file input-event-codes.h

        // Escape
        this.generateKeyRow(1, 1, -34, -10);

        this.generateKeyRow(2, 13, -31, -4);
        this.generateKeyRow(16, 27, -29, 0);
        this.generateKeyRow(30, 41, -27, 4);
        this.generateKeyRow(43, 53, -28, 8);

        // Function keys
        this.generateKeyRow(59, 62, -28, -10);
        this.generateKeyRow(63, 66, -15, -10);
        this.generateKeyRow(67, 70, -2, -10);

        // Left shift
        this.generateKeyRowWithKeyScaling(42,42, -27, 8, 0.115, 0);

        // Left alt
        this.generateKeyRowWithKeyScaling(56,56, -19, 12, 0.115, 0);

        // Space
        this.generateKeyRowWithKeyScaling(57,57, -1.6, 12, 0.75, 0);

    }

    private generateKeyRow(idFrom: number, idTo: number, startX: number, startZ: number) {
        for (let i = idFrom, x = startX; i <= idTo; i++, x += 3) {
            const key = Key.transform(x, startZ);
            this.keys.set(i, key);
        }
    }

    private generateKeyRowWithKeyScaling(idFrom: number, idTo: number, startX: number, startZ: number, xScale: number, xStep: number) {
        for (let i = idFrom, x = startX; i <= idTo; i++, x += xStep) {
            const key = Key.transformAndScaleX(x, startZ, xScale);
            this.keys.set(i, key);
        }
    }

    updateHeatmap(heatmap: any) {
        for (const [keyId, key] of this.keys) {
            const keypressCount = heatmap[keyId];

            if (keypressCount >= 1) {
                const value = Math.min(15, keypressCount - 1) / 15;

                const color1 = vec3.create();
                const color2 = vec3.create();

                vec3.scale(color1, END_COLOR, value);
                vec3.scale(color2, START_COLOR, 1.0 - value);

                vec3.add(color1, color1, color2);

                key.setColor(color1[0], color1[1], color1[2]);
            }
        }
    }
}