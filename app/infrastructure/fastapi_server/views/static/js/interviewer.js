const startButtom = document.querySelector("#startButton");
const stopButtom = document.querySelector("#stopButton");

var video_frames = [];

/**@type {WebSocket} */
let ws;
/**@type {number} */
let interval;

document.getElementById("toggleButtom").onclick = async (evt) => {
  /**@type {HTMLElement} */
  const buttom = evt.target;
  if (await verifyApplicants()) {
    alert("Postulante no conectado");
    return;
  }

  if (buttom.innerHTML === "Monitorear") {
    document.getElementById("feelings").classList.remove("d-none");
    buttom.innerHTML = "Detener";
    buttom.classList.remove("btn-success");
    buttom.classList.add("btn-danger");
    ws = new WebSocket("ws://localhost:8000/ws/interview");
    ws.onmessage = (evt) => {
      /**@type {{label: string, value: number}[]} */
      const data = JSON.parse(evt.data);
      data.forEach((feeling) => {
        const bar = document.getElementById(feeling.label);
        bar.style.width = `${feeling.value}%`;
        console.log(bar.style.width);
      });
      console.log(data);
    };
    interval = setInterval(() => {
      api.captureLargeVideoScreenshot().then((data) => {
        if (!data.dataURL) {
          return;
        }
        ws.send(JSON.stringify({ data: data.dataURL }));
      });
    }, 500);
  } else if (buttom.innerHTML === "Detener") {
    document.getElementById("feelings").classList.add("d-none");
    buttom.innerHTML = "Monitorear";
    buttom.classList.remove("btn-danger");
    buttom.classList.add("btn-success");
    if (ws) ws.close();
    if (interval) clearInterval(interval);
  }
};

const verifyApplicants = async () => {
  return !(await api
    .getParticipantsInfo()
    .some((participant) => !participant.formattedDisplayName.includes("me")));
};

document.getElementById("reportButtom").onclick = (evt) => {
  fetch("http://localhost:8000/feeling_report").then(async (response) => {
    const figure = document.getElementById("reportFig");
    const content = document.getElementById("modalBody");
    const dialog = document.getElementById("modalDialog");
    if (response.ok) {
      const data = await response.json();
      dialog.classList.add("modal-fullscreen");
      figure.classList.remove("d-none");
      content.innerHTML = "";
      content.appendChild(figure);
      figure.setAttribute("src", `data:image/jpg;base64,${data.data}`);
      return;
    }
    dialog.classList.remove("modal-fullscreen");
    figure.classList.add("d-none");
    content.innerHTML = `<div class="d-flex" ><svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="currentColor" class="bi bi-exclamation-square" viewBox="0 0 16 16">
      <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>
      <path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/>
    </svg> <h2 class="px-4" >Aun no se a generado ningun reporte</h2></div>`;
    content.appendChild(figure);
  });

  // figure.setAttribute("src", "data:image/jpg;base64,");
};
