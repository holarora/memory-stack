import { setCookie, getCookie } from '../cookie_utils';

// Mock the global alert and prompt functions
global.alert = jest.fn();
global.prompt = jest.fn();

describe('Cookie Functions', () => {
    beforeEach(() => {
        document.cookie = '';
        jest.clearAllMocks();
    });

    test('should set a cookie', () => {
        setCookie('testCookie', 'testValue', 1);

        const cookies = document.cookie.split('; ').reduce((acc, cookie) => {
            const [name, value] = cookie.split('=');
            acc[name] = value;
            return acc;
        }, {});

        expect(cookies['testCookie']).toBe('testValue');
    });

    test('should get a cookie', () => {
        document.cookie = 'testCookie=testValue';
        expect(getCookie('testCookie')).toBe('testValue');
    });

    test('should return an empty string for a non-existent cookie', () => {
        expect(getCookie('nonExistentCookie')).toBe('');
    });
});
