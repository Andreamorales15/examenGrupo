document
  .getElementById("formInstructor")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const nombrecompleto = document.getElementById("nombrecompleto").value;
    const correoelectronico =
      document.getElementById("correoelectronico").value;
    const sena = document.getElementById("sena").value;

    const data = {
      nombrecompleto: nombrecompleto,
      correoelectronico: correoelectronico,
      sena: sena,
    };

    fetch("/agregarinstructor/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.text())
      .then((html) => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");

        const alertContainer = doc.querySelector("#alert-container");
        const estado = alertContainer.getAttribute("data-estado");
        const mensaje = alertContainer.getAttribute("data-mensaje");

        if (estado === "True") {
          Swal.fire({
            icon: "success",
            title: "¡Éxito!",
            text: mensaje,
            confirmButtonText: "Aceptar",
          }).then(() => {
            window.location.href = "/";
          });
        } else {
          Swal.fire({
            icon: "error",
            title: "¡Error!",
            text: mensaje,
            confirmButtonText: "Aceptar",
          });
        }
      })
      .catch((error) => {
        Swal.fire({
          icon: "error",
          title: "¡Algo salió mal!",
          text: "Hubo un problema al procesar la solicitud.",
          confirmButtonText: "Aceptar",
        });
      });
  });
