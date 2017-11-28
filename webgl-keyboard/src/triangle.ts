
import {glMatrix, mat4, vec3} from "gl-matrix";
import {loadProgram} from "./utils";

const VERTEX_SHADER_SOURCE = `

attribute vec3 coordinate;
attribute vec3 color;

varying vec3 fragmentColor;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main() {
    fragmentColor = color;

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(coordinate, 1.0);
}
`;

const FRAGMENT_SHADER_SOURCE = `
precision mediump float;

varying vec3 fragmentColor;

void main() {
    gl_FragColor = vec4(fragmentColor, 1.0);
}

`;

const TRIANGLE_VERTICES = [
    -1.0,  1.0,  0.0,
     1.0, -1.0,  0.0,
    -1.0, -1.0,  0.0,
];

const TRIANGLE_VERTEX_COLORS = [
    1.0,  0.0,  0.0,
    0.0,  1.0,  0.0,
    0.0,  0.0,  1.0,
];

export class Triangle {
    public modelMatrix: mat4;
    constructor() {
        this.modelMatrix = mat4.create();
    }
}

export class TriangleRenderer {
    private triangleVertexAttributeData: WebGLBuffer;
    private triangleColorData: WebGLBuffer;

    constructor(gl: WebGLRenderingContext, private program: TriangleProgram) {
        this.triangleVertexAttributeData = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.triangleVertexAttributeData);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(TRIANGLE_VERTICES), gl.STATIC_DRAW);

        this.triangleColorData = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.triangleColorData);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(TRIANGLE_VERTEX_COLORS), gl.STATIC_DRAW);
    }

    render(gl: WebGLRenderingContext, triangle: Triangle, viewMatrix: mat4, projectionMatrix: mat4) {
        gl.bindBuffer(gl.ARRAY_BUFFER, this.triangleVertexAttributeData);

        gl.vertexAttribPointer(this.program.vertexAttribute, 3, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(this.program.vertexAttribute);

        gl.bindBuffer(gl.ARRAY_BUFFER, this.triangleColorData);

        gl.vertexAttribPointer(this.program.colorAttribute, 3, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(this.program.colorAttribute);

        gl.useProgram(this.program.program);

        gl.uniformMatrix4fv(this.program.viewMatrixUniform, false, viewMatrix);
        gl.uniformMatrix4fv(this.program.modelMatrixUniform, false, triangle.modelMatrix);
        gl.uniformMatrix4fv(this.program.projectionMatrixUniform, false, projectionMatrix);

        gl.drawArrays(gl.TRIANGLES, 0, 3);
    }
}

export class TriangleProgram {
    public vertexAttribute: number;
    public colorAttribute: number;
    public modelMatrixUniform: WebGLUniformLocation;
    public viewMatrixUniform: WebGLUniformLocation;
    public projectionMatrixUniform: WebGLUniformLocation;


    constructor(gl: WebGLRenderingContext, public program: WebGLProgram) {
        this.vertexAttribute = gl.getAttribLocation(program, "coordinate");
        this.colorAttribute = gl.getAttribLocation(program, "color");

        this.modelMatrixUniform = gl.getUniformLocation(program, "modelMatrix");
        this.viewMatrixUniform = gl.getUniformLocation(program, "viewMatrix");
        this.projectionMatrixUniform = gl.getUniformLocation(program, "projectionMatrix");
    }

    /**
     * Create TriangleProgram. Returns null if creation fails.
     * @param gl
     */
    static create(gl: WebGLRenderingContext): TriangleProgram {
        const program = loadProgram(gl, VERTEX_SHADER_SOURCE, FRAGMENT_SHADER_SOURCE);

        if (program === null) {
            return null;
        }

        return new TriangleProgram(gl, program);
    }
}