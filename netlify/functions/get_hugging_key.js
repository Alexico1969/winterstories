exports.handler = async function (event, context) {
    const key = process.env.HUGGING;
    if (!key) {
        return {
            statusCode: 404,
            body: JSON.stringify({ error: "HUGGING environment variable not found." })
        };
    }
    return {
        statusCode: 200,
        body: key
    };
};
