import { getCookie, setCookie } from "./cookie_utils.js";

export function showRandomEntry() {
    const today = new Date().toDateString();
    const lastPressDate = getCookie('lastPressDate');
    if (lastPressDate === today) {
        alert("今日のスタックがもうシャッフルされた. 🂱 \nPlease wait till tomorrow for another shuffle.✧₊⁺");
        return;
    }

    const entries = [...document.querySelectorAll('#hidden-older-entries li')];
    if (entries.length === 0) {
        alert("スタックを集めている段階です.もう少々お待ちください.｡°✩\nWe are currently in the process of organizing the stack. ⋆🎧");
        return;
    }

    const randomEntry = entries[Math.floor(Math.random() * entries.length)];
    if (!randomEntry) {
        console.error("Failed to select a random entry.");
        return;
    }
    const popup = document.getElementById('random-entry-popup');
    const overlay = document.getElementById('overlay');
    const finalCard = document.querySelector('.final-card');
    const cards = document.querySelectorAll('.card');
    const finalText = document.getElementById('final-text');

    finalCard.innerHTML = randomEntry.innerHTML;

    function hidePopupOnTap(event) {
        if (!popup.contains(event.target)) {
            popup.classList.add('hidden');
            overlay.classList.add('hidden');
            finalCard.classList.add('hidden');
            finalText.classList.add('hidden');
            document.removeEventListener('click', hidePopupOnTap);
        }
    }

    overlay.classList.remove('hidden');
    popup.classList.remove('hidden');
    cards.forEach(card => card.classList.remove('card-shuffle-animation'));
    finalCard.classList.remove('card-shuffle-animation');


    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.remove('hidden');
            card.classList.add('card-shuffle-animation');
        }, index * 300);
    });


    setTimeout(() => {
        finalCard.classList.remove('hidden');
        finalText.classList.remove('hidden');
        cards.forEach(card => card.classList.add('hidden'));
    }, 1200);

    setTimeout(() => {
        document.addEventListener('click', hidePopupOnTap);
    }, 3000);

    setCookie('lastPressDate', today, 1);
}

window.showRandomEntry = showRandomEntry;