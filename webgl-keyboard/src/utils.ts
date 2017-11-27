

/**
 * Creates WebGL program. Returns null if program creation failed.
 * @param gl
 * @param vertexShaderSource
 * @param fragmentShaderSource
 */
export function loadProgram(gl: WebGLRenderingContext, vertexShaderSource: string, fragmentShaderSource: string): WebGLProgram {
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

/**
 * Creates WebGL shader. Returns null if shader creation failed.
 * @param gl
 * @param shaderType
 * @param sourceCode
 */
export function loadShader(gl: WebGLRenderingContext, shaderType: number, sourceCode: string): WebGLShader {
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
