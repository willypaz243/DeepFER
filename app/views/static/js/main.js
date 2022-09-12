var domain = "meet.jit.si";
var options = {
  roomName: "Embed",
  width: 1080,
  height: 720,
  parentNode: document.querySelector("#meet"),
  interfaceConfigOverwrite: {
    TOOLBAR_BUTTONS: [
      "microphone",
      "camera",
      "filmstrip",
      "settings",
      "hangup",
    ],
    MAIN_TOOLBAR_BUTTONS: ["microphone", "camera"],
  },
  p2p: {
    enabled: true,
  },
};
var api = new JitsiMeetExternalAPI(domain, options);
