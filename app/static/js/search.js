document.getElementById('sortOptions').addEventListener('change', function () {
        const sortValue = this.value
        const [field, order] = sortValue.split('-');
        const container = document.getElementById('cardsContainer');
        const cards = Array.from(container.getElementsByClassName('card-item'));

        // Sorteeri kaardid
        cards.sort((a, b) => {
            let valA = a.dataset[field];
            let valB = b.dataset[field];

            // Muuda numbriväljad arvudeks
            if (field === 'capital' || field === 'registry') {
                valA = parseInt(valA, 10);
                valB = parseInt(valB, 10);
            }

            if (order === 'asc') {
                return valA > valB ? 1 : -1;
            } else {
                return valA < valB ? 1 : -1;
            }
        });

        // Lisa sorteeritud kaardid uuesti konteinerisse
        container.innerHTML = '';
        cards.forEach(card => container.appendChild(card));
    })