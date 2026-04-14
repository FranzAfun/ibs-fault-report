(() => {
    const modal = document.getElementById('deleteConfirmModal');
    if (!modal) {
        return;
    }

    const form = document.getElementById('deleteConfirmForm');
    const targetTypeLabel = document.getElementById('delete-modal-target-type');
    const referenceLabel = document.getElementById('delete-modal-reference');
    const nextInput = document.getElementById('delete-modal-next');
    const submitButton = document.getElementById('delete-modal-submit');
    const cancelButtons = modal.querySelectorAll('.js-modal-cancel');
    let lastTrigger = null;

    const openModal = (trigger) => {
        const deleteUrl = trigger.getAttribute('data-delete-url');
        const reference = trigger.getAttribute('data-reference') || 'selected item';
        const deleteType = trigger.getAttribute('data-delete-type') || 'item';
        const buttonText = trigger.getAttribute('data-delete-button') || 'Delete';
        const nextUrl = trigger.getAttribute('data-next-url') || '';

        if (!deleteUrl || !form || !referenceLabel || !targetTypeLabel) {
            return;
        }

        lastTrigger = trigger;
        form.setAttribute('action', deleteUrl);
        referenceLabel.textContent = reference;
        targetTypeLabel.textContent = deleteType;

        if (nextInput) {
            nextInput.value = nextUrl;
        }

        if (submitButton) {
            submitButton.textContent = buttonText;
        }

        modal.hidden = false;
        document.body.classList.add('modal-open');

        const primaryButton = form.querySelector('button[type="submit"]');
        if (primaryButton) {
            primaryButton.focus();
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

        if (targetTypeLabel) {
            targetTypeLabel.textContent = 'item';
        }

        if (nextInput) {
            nextInput.value = '';
        }

        if (submitButton) {
            submitButton.textContent = 'Delete';
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
