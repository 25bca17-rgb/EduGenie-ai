async function askQuestion() {

    const question = document.getElementById("question").value;
    const answerBox = document.getElementById("answer");

    if (!question.trim()) {
        answerBox.innerText = "Please enter a question.";
        return;
    }

    answerBox.innerText = "Thinking...";

    try {

        const response = await fetch("/qa", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        answerBox.innerText = data.answer;

    } catch (error) {

        answerBox.innerText =
            "Error connecting to EduGenie.";

        console.error(error);
    }
}