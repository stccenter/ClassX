declare global {

    interface Link {
        name: string;
        url: string;
    }

    interface ImportMeta {
        env: {
            VITE_CDN_URL: string;
            VITE_SRC_URL: string
        };
    }
}

export { };
