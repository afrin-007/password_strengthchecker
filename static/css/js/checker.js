const passwordInput = document.getElementById("password");
passwordInput.addEventListener("input", async () => {
try {
const response = await fetch("/analyze", {
method: "POST",
headers: {
"Content-Type": "application/json"
},
body: JSON.stringify({
password: passwordInput.value
})
});
const data = await response.json();
document.getElementById("fill").style.width = `${data.score * 20}%`;
document.getElementById("score").innerText =
`Strength Score: ${data.score}/5`;
document.getElementById("entropy").innerText =
`Entropy: ${data.entropy}`;
document.getElementById("crack").innerText =
`Estimated Crack Time: ${data.crack_time}`;
document.getElementById("suggestions").innerHTML =
data.suggestions.map(s => `<li>${s}</li>`).join("");
} catch (error) {
console.error("Error:", error);
}
});
