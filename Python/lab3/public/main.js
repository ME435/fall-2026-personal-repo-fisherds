async function sendCommand(command) {
    let response = await fetch(`/api/${command}`);
    let replyText = await response.text();
    console.log(replyText);

    document.querySelector("#replyText").innerHTML = replyText;

    return replyText;
}

function main() {
    console.log("Hello JavaScript");
    // document.querySelector("#reset").innerHTML = "Hello";

    document.querySelector("#reset").onclick = () => {
        sendCommand("RESET");
    };

    document.querySelector("#x1").onclick = () => {
        sendCommand("X-AXIS 1");
    };
    document.querySelector("#x2").onclick = () => {
        sendCommand("X-AXIS 2");
    };
    document.querySelector("#x3").onclick = () => {
        sendCommand("X-AXIS 3");
    };
    document.querySelector("#x4").onclick = () => {
        sendCommand("X-AXIS 4");
    };
    document.querySelector("#x5").onclick = () => {
        sendCommand("X-AXIS 5");
    };

    document.querySelector("#gOpen").onclick = () => {
        sendCommand("GRIPPER OPEN");
    };
    document.querySelector("#gClose").onclick = () => {
        sendCommand("GRIPPER CLOSE");
    };

    document.querySelector("#move").onclick = () => {
      let startPos = document.querySelector("#moveFrom").value;
      let endPos = document.querySelector("#moveTo").value;
      sendCommand(`MOVE ${startPos} ${endPos}`);
      
    }

}


main();
