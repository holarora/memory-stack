import { setCookie, getCookie, clearCookies } from '../cookie_utils';
import { showRandomEntry } from '../randomEntry';

import { jest } from '@jest/globals';

global.alert = jest.fn();
global.console.error = jest.fn();

function setUpDOM() {
    document.body.innerHTML = `
        <div class="shuffle-button" onclick="showRandomEntry()"></div>
        <div id="random-entry-popup" class="entry-popup hidden">
            <div id="card-container">
                <div class="card blank-card"></div>
                <div class="card blank-card"></div>
                <div class="final-card hidden"></div>
                <div class="final-text hidden" id="final-text">
                    今日のスタックがシャッフルされた <br>
                    Please wait till tomorrow for another shuffle <br>
                    - - - - -
                </div>
            </div>
        </div>
        <div id="overlay" class="overlay hidden"></div>
        <ul id="hidden-older-entries">
            <li>Entry 1</li>
            <li>Entry 2</li>
            <li>Entry 3</li>
        </ul>
    `;
}

describe('showRandomEntry', () => {
    beforeEach(() => {
        setUpDOM();
        jest.clearAllMocks();
    });

    test('should alert and return if shuffle is attempted on the same day', () => {
        setCookie('lastPressDate', new Date().toDateString(), 1);

        showRandomEntry();

        expect(global.alert).toHaveBeenCalledWith(
            "今日のスタックがもうシャッフルされた. 🂱 \nPlease wait till tomorrow for another shuffle.✧₊⁺"
        );
        expect(global.console.error).not.toHaveBeenCalled();
    });

    test('should shuffle and display a random entry', () => {
        jest.spyOn(global.Date.prototype, 'toDateString').mockReturnValue('2024-09-10');
        setCookie('lastPressDate', '2000-01-01', 1);

        showRandomEntry();

        const entries = document.querySelectorAll('#hidden-older-entries li');
        expect(entries.length).toBeGreaterThan(0);
        expect(document.getElementById('random-entry-popup').classList.contains('hidden')).toBe(false);
        expect(document.getElementById('card-container').classList.contains('hidden')).toBe(false);
    });

    test('should handle no extra entries gracefully', () => {
        document.getElementById('hidden-older-entries').innerHTML = '';
        setCookie('lastPressDate', '2000-01-01', 1);

        showRandomEntry();

        expect(global.alert).toHaveBeenCalledWith(
            "スタックを集めている段階です.もう少々お待ちください.｡°✩\nWe are currently in the process of organizing the stack. ⋆🎧"
        );
        expect(global.console.error).not.toHaveBeenCalled();
    });
});
