exports.handler = async function(event, context) {
  const key = process.env.ELEVEN;
  if (!key) {
    return {
      statusCode: 404,
      body: JSON.stringify({ error: "ELEVEN environment variable not found." })
    };
  }
  return {
    statusCode: 200,
    body: key
  };
};
