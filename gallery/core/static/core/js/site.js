document.documentElement.classList.add('js-ready');

document.querySelectorAll('[data-tab-target]').forEach((tabButton) => {
	tabButton.addEventListener('click', () => {
		const tabsPanel = tabButton.closest('.detail-tabs-panel');
		if (!tabsPanel) {
			return;
		}

		const targetName = tabButton.getAttribute('data-tab-target');
		if (!targetName) {
			return;
		}

		tabsPanel.querySelectorAll('[data-tab-target]').forEach((button) => {
			const isActive = button === tabButton;
			button.classList.toggle('is-active', isActive);
			button.setAttribute('aria-selected', String(isActive));
		});

		tabsPanel.querySelectorAll('[data-tab-panel]').forEach((panel) => {
			panel.classList.toggle('is-active', panel.getAttribute('data-tab-panel') === targetName);
		});
	});
});