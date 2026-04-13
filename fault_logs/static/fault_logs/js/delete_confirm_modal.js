(() => {
    const modal = document.getElementById('deleteConfirmModal');
    if (!modal) {
        return;
    }

    const form = document.getElementById('deleteConfirmForm');
    const referenceLabel = document.getElementById('delete-modal-reference');
    const cancelButtons = modal.querySelectorAll('.js-modal-cancel');
    let lastTrigger = null;

    const openModal = (trigger) => {
        const deleteUrl = trigger.getAttribute('data-delete-url');
        const reference = trigger.getAttribute('data-reference') || 'selected report';
        if (!deleteUrl || !form || !referenceLabel) {
            return;
        }

        lastTrigger = trigger;
        form.setAttribute('action', deleteUrl);
        referenceLabel.textContent = reference;
        modal.hidden = false;
        document.body.classList.add('modal-open');

        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.focus();
        }
    };

    const closeModal = () => {
        modal.hidden = true;
        document.body.classList.remove('modal-open');

        if (form) {
            form.removeAttribute('action');
        }

        if (referenceLabel) {
            referenceLabel.textContent = '';
        }

        if (lastTrigger) {
            lastTrigger.focus();
            lastTrigger = null;
        }
    };

    document.addEventListener('click', (event) => {
        const trigger = event.target.closest('.js-delete-trigger');
        if (trigger) {
            event.preventDefault();
            openModal(trigger);
            return;
        }

        if (event.target === modal) {
            closeModal();
        }
    });

    cancelButtons.forEach((button) => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            closeModal();
        });
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && !modal.hidden) {
            closeModal();
        }
    });
})();
