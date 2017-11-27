
import {glMatrix, mat4, vec3} from "gl-matrix";

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

class Triangle {
    public modelMatrix: mat4;
    constructor() {
        this.modelMatrix = mat4.create();
    }
}

class TriangleProgram {
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
}

export class Renderer {
    private projectionMatrix: mat4;
    private viewMatrix: mat4;
    private triangle: Triangle;
    private triangleVertexAttributeData: WebGLBuffer;
    private triangleColorData: WebGLBuffer;
    private triangleProgram: TriangleProgram;

    constructor(private gl: WebGLRenderingContext, program: WebGLProgram) {
        this.projectionMatrix = mat4.create();
        mat4.perspective(this.projectionMatrix, 45 * Math.PI / 180, gl.canvas.width/gl.canvas.height, 0.1, 100);

        this.viewMatrix = mat4.create();
        mat4.lookAt(this.viewMatrix, [0,0,5], [0,0,0], [0,1,0]);

        this.triangle = new Triangle();

        this.triangleVertexAttributeData = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.triangleVertexAttributeData);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(TRIANGLE_VERTICES), gl.STATIC_DRAW);

        this.triangleColorData = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.triangleColorData);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(TRIANGLE_VERTEX_COLORS), gl.STATIC_DRAW);


        gl.clearColor(0, 0, 0, 1);
        gl.enable(gl.DEPTH_TEST);

        this.triangleProgram = new TriangleProgram(gl, program);
    }

    static create(gl: WebGLRenderingContext): Renderer {
        const program = loadProgram(gl, VERTEX_SHADER_SOURCE, FRAGMENT_SHADER_SOURCE);

        if (program === null) {
            return null;
        }

        return new Renderer(gl, program);
    }

    draw() {
        const gl = this.gl;

        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

        gl.bindBuffer(gl.ARRAY_BUFFER, this.triangleVertexAttributeData);

        gl.vertexAttribPointer(this.triangleProgram.vertexAttribute, 3, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(this.triangleProgram.vertexAttribute);

        gl.bindBuffer(gl.ARRAY_BUFFER, this.triangleColorData);

        gl.vertexAttribPointer(this.triangleProgram.colorAttribute, 3, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(this.triangleProgram.colorAttribute);

        gl.useProgram(this.triangleProgram.program);

        gl.uniformMatrix4fv(this.triangleProgram.viewMatrixUniform, false, this.viewMatrix);
        gl.uniformMatrix4fv(this.triangleProgram.modelMatrixUniform, false, this.triangle.modelMatrix);
        gl.uniformMatrix4fv(this.triangleProgram.projectionMatrixUniform, false, this.projectionMatrix);


        gl.drawArrays(gl.TRIANGLES, 0, 3);
    }
}

function loadProgram(gl: WebGLRenderingContext, vertexShaderSource: string, fragmentShaderSource: string): WebGLProgram {
    const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vertexShaderSource);

    if (vertexShader === null) {
        return null;
    }

    const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);

    if (fragmentShader === null) {
        gl.deleteShader(vertexShader);
        return null;
    }

    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);

    gl.deleteShader(vertexShader);
    gl.deleteShader(fragmentShader);

    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        const errorMessage = gl.getProgramInfoLog(program);
        console.error(`Program linking error: ${errorMessage}`);
        gl.deleteProgram(program);
        return null;
    }

    return program;
}

function loadShader(gl: WebGLRenderingContext, shaderType: number, sourceCode: string): WebGLShader {
    const shader = gl.createShader(shaderType);
    gl.shaderSource(shader, sourceCode);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        const errorMessage = gl.getShaderInfoLog(shader);
        console.error(`Shader compile error: ${errorMessage}`);
        gl.deleteShader(shader);
        return null;
    }

    return shader;
}
