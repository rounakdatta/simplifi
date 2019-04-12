onmessage = function (e) {
    let output = [];
    const INPUT = JSON.parse(e.data.input);
    try {
        eval(`
            console.log = function (str) {
                output.push(str)
            }

            ${e.data.code}
            `);
    } catch (e) {
        output.push(`Error : ${e}`);
    } finally {
        postMessage(output)
    }
};
