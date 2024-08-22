function sendVote(choice) {
    // Play vote animation
    if (choice === "yes") {
        const btnYes = document.querySelector("#btnYes");
        const plusOne = document.createElement("div");
        const plusOneDiv = document.createElement("div");
        plusOne.appendChild(plusOneDiv);
        btnYes.appendChild(plusOne);
        plusOne.className = "plusOne";
        plusOneDiv.textContent = "+1"
        setTimeout(() => { plusOne.remove() }, 3100);
    } else {
        const btnNo = document.querySelector("#btnNo");
        const minusOne = document.createElement("div");
        const minusOneDiv = document.createElement("div");
        minusOne.appendChild(minusOneDiv);
        btnNo.appendChild(minusOne);
        minusOne.className = "minusOne";
        minusOneDiv.textContent = "-1"
        setTimeout(() => { minusOne.remove() }, 3100);
    }

    const request = new XMLHttpRequest();
    request.open("POST", "/vote");
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.onload = (event) => {
        const blob = request.response;
        console.log(blob);
    };

    // Animation for vote share bar
    request.send(JSON.stringify({ "choice": choice }));
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200 && !document.querySelector(".VoteShareYes")) {
            const votesArray = request.responseText.replace('"', '').split(",");
            const yesVotes = votesArray[0];
            const noVotes = votesArray[1];
            const denominator = parseInt(yesVotes) + parseInt(noVotes);
            const votePercentage = yesVotes / denominator;
            const voteContainer = document.createElement("div");
            voteContainer.className = "VoteContainer";

            const yesDiv = document.createElement("div");
            yesDiv.className = "VoteShareYes";
            const p = document.createElement("p");
            p.textContent = votePercentage * 100 + "% Art";
            yesDiv.appendChild(p)
            const noDiv = document.createElement("div");
            noDiv.className = "VoteShareNo";
            const p2 = document.createElement("p");
            p2.textContent = (1 - votePercentage) * 100 + "% Fart";
            noDiv.appendChild(p2)

            voteContainer.appendChild(yesDiv);
            voteContainer.appendChild(noDiv);

            document.body.appendChild(voteContainer);

            animateVoteBar(voteContainer, votePercentage);
        }
    }
}

function animateVoteBar(container, stoppingPoint) {
    let leftElement = document.querySelector(".VoteShareYes");
    leftElement.style.width = 0;
    let leftAccel = 6;
    let leftVelocity = 0;

    let rightElement = document.querySelector(".VoteShareNo");
    rightElement.style.width = 0;
    let rightAccel = 6;
    let rightVelocity = 0;

    let delta;

    const zero = performance.now(); // The only timestamp
    let lastTime = 0; // ms relative to zero
    requestAnimationFrame(animate);

    function animate(timeStamp) {
        // No negative times (this can happen the first iteration)
        const currentTime = Math.max(0, (timeStamp - zero));
        delta = currentTime - lastTime;
        lastTime = currentTime;

        if (currentTime < 3000) {
            leftVelocity += leftAccel * delta / 16;
            leftElement.style.width = (leftElement.clientWidth + leftVelocity) + "px";
            let leftCurrentWidth = leftElement.clientWidth;

            let leftStopPixels = container.clientWidth * stoppingPoint;
            if (leftCurrentWidth > leftStopPixels) {
                leftElement.style.width = leftStopPixels;
                leftVelocity *= -.5;
            }

            rightVelocity += rightAccel * delta / 16;
            rightElement.style.width = (rightElement.clientWidth + rightVelocity) + "px";
            let rightCurrentWidth = rightElement.clientWidth;

            let rightStopPixels = container.clientWidth * (1 - stoppingPoint);
            if (rightCurrentWidth > rightStopPixels) {
                rightElement.style.width = rightStopPixels;
                rightVelocity *= -.5;
                // TODO: Create particles at stop point
            }

            requestAnimationFrame(animate);
        } else {
            leftElement.style.width = stoppingPoint * 100 + "%";
            rightElement.style.width = (1 - stoppingPoint) * 100 + "%";
        }
    }
}

function onImageLoaded() {
    // Scale image. Try nice then try mean.
    let initialWindowWidth = window.visualViewport.width;
    let initialWindowHeight = window.visualViewport.height;
    
    art.aspectRatio = art.naturalWidth/art.naturalHeight;

    if (art.naturalWidth > art.naturalHeight) {
        art.width = initialWindowWidth * .70;
        art.height = art.width / art.aspectRatio;
    } else {
        art.height = initialWindowHeight * .70;
        art.width = art.height * art.aspectRatio;
    }

    if (art.width > initialWindowWidth || art.height > initialWindowHeight) {
        if (art.width > initialWindowWidth) {
            art.width = initialWindowWidth;
            art.height = art.width / art.aspectRatio;
        } else {
            art.height = initialWindowHeight;
            art.width = art.height * art.aspectRatio;
        }
    }
};

document.addEventListener("DOMContentLoaded", () => {
    var art = document.querySelector("#art");

    if (art.complete) {
        onImageLoaded()
    } else {
        art.addEventListener("load", onImageLoaded);
    }

    screen.orientation.onchange = () => {
        function orientationResizeEvent() {
            onImageLoaded();
            window.removeEventListener("resize", orientationResizeEvent);
        }
        window.addEventListener("resize", orientationResizeEvent);
    }; // To get the updated height we need the orientation listener and the resize listener together.

    document.querySelector("#btnYes").addEventListener("click", () => sendVote("yes"));
    document.querySelector("#btnNo").addEventListener("click", () => sendVote("no"));
});
