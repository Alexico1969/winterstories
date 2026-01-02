exports.handler = async function (event, context) {
    const key = process.env.OPENAI;
    if (!key) {
        return {
            statusCode: 404,
            body: JSON.stringify({ error: "OPENAI environment variable not found." })
        };
    }
    return {
        statusCode: 200,
        body: key
    };
};
