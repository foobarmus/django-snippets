function focus() {
    q = document.forms.search.q;
    if (!q.value) {
        q.focus();
    }
}

function validate(form) {
    return form.q.value ? true : false;
}
