document
  .getElementById("formGuia")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const nombreguia = document.getElementById("nombreguia").value;
    const descripcion = document.getElementById("descripcion").value;
    const programaformacion = document.getElementById("programaformacion").value;
    const fecha = document.getElementById("fecha").value;
    const instructor_id = document.getElementById("instructor_id").value;
    const archivo = document.getElementById("documento").files[0];

    const formData = new FormData();
    formData.append("nombreguia", nombreguia);
    formData.append("descripcion", descripcion);
    formData.append("programaformacion", programaformacion);
    formData.append("fecha", fecha);
    formData.append("instructor_id", instructor_id);
    formData.append("documento", archivo);

    fetch("/agregarguia/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.text())
      .then((html) => {
        document.body.innerHTML = html;
      })
      .catch((error) => {
        alert("¡Algo salió mal! Hubo un problema al procesar la solicitud.");
      });
  });
