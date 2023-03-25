class MainModal {

    constructor() {

        if (typeof MainModal.instance === 'object') {
          return MainModal.instance.clear();
        }

        MainModal.instance = this;

        this.modal = new bootstrap.Modal(document.getElementById("mainModal"), {});
        this.title = document.querySelector("#mainModal .modal-title");
        this.body = document.querySelector("#mainModal .modal-body");
        this.footer = document.querySelector("#mainModal .modal-footer");
    }

    setTitle(title) {
        this.title.innerText = title
        return this
    }

    addToBody(val) {
        this.body.innerHTML += val
        return this
    }

    addToFooter(val) {
        this.footer.innerHTML += val;
        return this
    }

    addFooterCloseButton(text="Close") {
        this.addToFooter('<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">' + text + '</button>');
        return this
    }

    show() {
        this.modal.show();
        return this;
    }

    hide() {
        this.modal.hide();
        return this;
    }

    clear() {
        this.setTitle("");
        this.footer.innerHTML = "";
        this.body.innerHTML = "";
        return this;
    }

}