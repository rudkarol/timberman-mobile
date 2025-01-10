export class AssetLoader {
    static async loadAssets() {
        const assetUrls = {
            tree0: 'assets/textures/tree0.png',
            tree1: 'assets/textures/tree1.png',
            tree2: 'assets/textures/tree2.png',
            player: 'assets/textures/player.png',
            player1: 'assets/textures/player1.png',
            background: 'assets/textures/background.png',
        };

        const assets = {};
        const loadPromises = Object.entries(assetUrls).map(async ([key, url]) => {
            assets[key] = await this.loadImage(url);
        });

        await Promise.all(loadPromises);
        return assets;
    }

    static loadImage(url) {
        return new Promise((resolve) => {
            const img = new Image();
            img.src = url;
            img.onload = () => resolve(img);
        });
    }
}
