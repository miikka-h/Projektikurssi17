
import {glMatrix, mat4, vec3, vec4} from "gl-matrix";
import {loadProgram} from "./utils";

const VERTEX_SHADER_SOURCE = `

attribute vec3 coordinate;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main() {
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(coordinate, 1.0);
}
`;

const FRAGMENT_SHADER_SOURCE = `
precision mediump float;

uniform vec3 color;

void main() {
    gl_FragColor = vec4(color, 1.0);
}

`;

// Side face at z = 1.0
const CUBE_FACE_VERTICES = [
    // Triangle 1
   -1.0,  1.0,  1.0,
    1.0, -1.0,  1.0,
   -1.0, -1.0,  1.0,

    // Triangle 2
   -1.0,  1.0,  1.0,
    1.0,  1.0,  1.0,
    1.0, -1.0,  1.0,
];

function cubeFaceTransform(matrix: mat4): number[] {
    let vec = vec4.create();
    let bufferVec = vec4.create();

    let newVertices = [];

    for (let i = 0;  i < CUBE_FACE_VERTICES.length; i+= 3) {
        vec4.set(vec, CUBE_FACE_VERTICES[i], CUBE_FACE_VERTICES[i+1], CUBE_FACE_VERTICES[i+2], 1.0);

        vec4.transformMat4(bufferVec, vec, matrix);
        newVertices.push(bufferVec[0], bufferVec[1], bufferVec[2]);
    }

    return newVertices;
}

function pushAll(from: number[], to: number[]) {
    for (let x of from) {
        to.push(x);
    }
}

/**
 * Return all faces except top face.
 */
function createCubeSideVertices(): number[] {
    let vertices: number[] = [];

    let matrix = mat4.create();

    pushAll(CUBE_FACE_VERTICES, vertices);

    mat4.fromYRotation(matrix, Math.PI/2.0);
    pushAll(cubeFaceTransform(matrix), vertices);

    mat4.fromYRotation(matrix, Math.PI);
    pushAll(cubeFaceTransform(matrix), vertices);

    mat4.fromYRotation(matrix, Math.PI * 1.5);
    pushAll(cubeFaceTransform(matrix), vertices);

    mat4.fromXRotation(matrix, Math.PI/2.0);
    pushAll(cubeFaceTransform(matrix), vertices);

    return vertices;
}

const CUBE_SIDE_VERTICES = createCubeSideVertices();


function createCubeTopFace(): number[] {
    let vertices: number[] = [];

    let matrix = mat4.create();

    mat4.fromXRotation(matrix, -Math.PI/2.0);
    pushAll(cubeFaceTransform(matrix), vertices);

    return vertices;
}

const CUBE_TOP_VERTICES = createCubeTopFace();

export class Cube {
    public modelMatrix: mat4;
    public topFaceColor: vec3;
    public sideFaceColor: vec3;

    constructor() {
        this.modelMatrix = mat4.create();

        this.topFaceColor = vec3.create();
        vec3.set(this.topFaceColor, 0.5, 0.5, 0.5);

        this.sideFaceColor = vec3.create();
        vec3.set(this.sideFaceColor, 0.3, 0.3, 0.3);
    }
}

export class CubeRenderer {
    private vertices: WebGLBuffer;
    private topVertices: WebGLBuffer;

    constructor(gl: WebGLRenderingContext, private program: CubeProgram) {
        this.vertices = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.vertices);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(CUBE_SIDE_VERTICES), gl.STATIC_DRAW);

        this.topVertices = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.topVertices);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(CUBE_TOP_VERTICES), gl.STATIC_DRAW);
    }

    render(gl: WebGLRenderingContext, cube: Cube, viewMatrix: mat4, projectionMatrix: mat4) {

        // Draw cube side faces.

        gl.bindBuffer(gl.ARRAY_BUFFER, this.vertices);

        gl.vertexAttribPointer(this.program.vertexAttribute, 3, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(this.program.vertexAttribute);

        gl.useProgram(this.program.program);

        gl.uniformMatrix4fv(this.program.viewMatrixUniform, false, viewMatrix);
        gl.uniformMatrix4fv(this.program.modelMatrixUniform, false, cube.modelMatrix);
        gl.uniformMatrix4fv(this.program.projectionMatrixUniform, false, projectionMatrix);
        gl.uniform3fv(this.program.colorUniform, cube.sideFaceColor);

        gl.drawArrays(gl.TRIANGLES, 0, CUBE_SIDE_VERTICES.length/3.0);


        // Draw cube top face.

        gl.bindBuffer(gl.ARRAY_BUFFER, this.topVertices);

        gl.vertexAttribPointer(this.program.vertexAttribute, 3, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(this.program.vertexAttribute);

        gl.useProgram(this.program.program);

        gl.uniformMatrix4fv(this.program.viewMatrixUniform, false, viewMatrix);
        gl.uniformMatrix4fv(this.program.modelMatrixUniform, false, cube.modelMatrix);
        gl.uniformMatrix4fv(this.program.projectionMatrixUniform, false, projectionMatrix);
        gl.uniform3fv(this.program.colorUniform, cube.topFaceColor);

        gl.drawArrays(gl.TRIANGLES, 0, CUBE_TOP_VERTICES.length/3.0);

    }
}

export class CubeProgram {
    public vertexAttribute: number;
    public modelMatrixUniform: WebGLUniformLocation;
    public viewMatrixUniform: WebGLUniformLocation;
    public projectionMatrixUniform: WebGLUniformLocation;
    public colorUniform: WebGLUniformLocation;


    constructor(gl: WebGLRenderingContext, public program: WebGLProgram) {
        this.vertexAttribute = gl.getAttribLocation(program, "coordinate");

        this.modelMatrixUniform = gl.getUniformLocation(program, "modelMatrix");
        this.viewMatrixUniform = gl.getUniformLocation(program, "viewMatrix");
        this.projectionMatrixUniform = gl.getUniformLocation(program, "projectionMatrix");
        this.colorUniform = gl.getUniformLocation(program, "color");

    }

    /**
     * Create TriangleProgram. Returns null if creation fails.
     * @param gl
     */
    static create(gl: WebGLRenderingContext): CubeProgram {
        const program = loadProgram(gl, VERTEX_SHADER_SOURCE, FRAGMENT_SHADER_SOURCE);

        if (program === null) {
            return null;
        }

        return new CubeProgram(gl, program);
    }
}