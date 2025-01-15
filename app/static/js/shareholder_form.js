document.addEventListener("DOMContentLoaded", function () {
    const tbody = document.getElementById("shareholders-body");
    const typeSelector = document.getElementById("shareholder-type");
    const individualFields = document.querySelector(".individual-fields");
    const legalFields = document.querySelector(".legal-fields");

    function toggleFormFields() {
        const isIndividual = typeSelector.value === "individual";
        individualFields.classList.toggle("d-none", !isIndividual);
        legalFields.classList.toggle("d-none", isIndividual);
    }

    typeSelector.addEventListener("change", toggleFormFields);
    toggleFormFields();

    const confirmButton = document.getElementById("confirm-shareholder");
    confirmButton.addEventListener("click", function () {
        const errors = [];
        const firstName = document.getElementById("first_name").value.trim();
        const lastName = document.getElementById("last_name").value.trim();
        const personalCode = document.getElementById("personal_code").value.trim();
        const companyName = document.getElementById("company_name").value.trim();
        const legalRegistryCode = document.getElementById("legal_registry_code").value.trim();
        const share = document.getElementById("share").value.trim();

        // Valideerimine
        if (typeSelector.value === "individual") {
            if (!firstName) errors.push("Eesnimi on kohustuslik!");
            if (!lastName) errors.push("Perekonnanimi on kohustuslik!");
            if (!personalCode) errors.push("Isikukood on kohustuslik!");
        } else {
            if (!companyName) errors.push("Ärinimi on kohustuslik!");
            if (!legalRegistryCode) errors.push("Registrikood on kohustuslik!");
        }

        if (!share || isNaN(share) || parseFloat(share) < 1) {
            errors.push("Osa suurus peab olema vähemalt 1€.");
        }

        const errorContainer = document.getElementById("error-alert-container");
        if (errors.length > 0) {
            errorContainer.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <ul class="mb-0">${errors.map(e => `<li>${e}</li>`).join("")}</ul>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>`;
        } else {
            const newIndex = tbody.children.length;
            const isIndividual = typeSelector.value === "individual";
            const identifier = isIndividual ? personalCode : legalRegistryCode;
            const name = isIndividual ? `${firstName} ${lastName}` : companyName;

            // Lisa uus rida tabelisse
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>
                        ${isIndividual ? "Füüsiline isik" : "Juriidiline isik"}
                     <input type="hidden" name="shareholders-${newIndex}-is_individual" value="${isIndividual ? "individual" : "legal"}">
                    </td>
                <td><input type="text" class="form-control" name="shareholders-${newIndex}-first_name" value="${isIndividual ? firstName : ""}" ${!isIndividual ? "disabled" : ""}></td>
                <td><input type="text" class="form-control" name="shareholders-${newIndex}-last_name" value="${isIndividual ? lastName : ""}" ${!isIndividual ? "disabled" : ""}></td>
                <td><input type="text" class="form-control" name="shareholders-${newIndex}-company_name" value="${!isIndividual ? companyName : ""}" ${isIndividual ? "disabled" : ""}></td>
                <td><input type="text" class="form-control" name="shareholders-${newIndex}-registry_code" value="${!isIndividual ? legalRegistryCode : ""}" ${isIndividual ? "disabled" : ""}></td>
                <td><input type="text" class="form-control" name="shareholders-${newIndex}-personal_code" value="${isIndividual ? personalCode : ""}" ${!isIndividual ? "disabled" : ""}></td>
                <td><input type="number" class="form-control" name="shareholders-${newIndex}-share" value="${share}"></td>
                <td><input type="checkbox"  name="shareholders-${newIndex}-is_founder" checked></td>
                <td><button type="button" class="btn btn-danger btn-sm remove-row">Eemalda</button></td>
            `;
            tbody.appendChild(tr);

            // Puhasta vead ja vorm
            errorContainer.innerHTML = `<div class="alert alert-success">Osanik lisatud edukalt!</div>`;
            document.getElementById("first_name").value = "";
            document.getElementById("last_name").value = "";
            document.getElementById("personal_code").value = "";
            document.getElementById("company_name").value = "";
            document.getElementById("legal_registry_code").value = "";
            document.getElementById("share").value = "";
            typeSelector.value = "individual";
            toggleFormFields();
        }
    });

    // Eemalda rea funktsioon
    tbody.addEventListener("click", function (event) {
        if (event.target.classList.contains("remove-row")) {
            const row = event.target.closest("tr");
            row.remove();
        }
    });
});
