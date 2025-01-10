import { GameConfig } from './config.js';

export class Renderer {
    constructor(ctx, assets) {
        this.ctx = ctx;
        this.assets = assets;
        this.treeCenterX = GameConfig.CANVAS.WIDTH / 2;
    }

    clearScreen() {
        this.ctx.clearRect(0, 0, GameConfig.CANVAS.WIDTH, GameConfig.CANVAS.HEIGHT);
    }

    drawBackground() {
        this.ctx.drawImage(this.assets.background, 0, 0, GameConfig.CANVAS.WIDTH, GameConfig.CANVAS.HEIGHT);
    }

    drawTree(tree) {
        let posY = GameConfig.TREE.START_POS_Y;

        for (let i = 0; i < GameConfig.TREE.SEGMENTS; i++) {
            const node = tree.get(i);
            const img = this.assets[`tree${node}`];
            const segmentWidth = node === 0 ? GameConfig.TREE.BASE_WIDTH : GameConfig.TREE.BRANCH_WIDTH;
            
            const treeX = this.treeCenterX - (GameConfig.TREE.BASE_WIDTH / 2);
            const xOffset = node === 0 ? 0 : (GameConfig.TREE.BRANCH_WIDTH - GameConfig.TREE.BASE_WIDTH) / 2;
            
            this.ctx.drawImage(img, treeX - xOffset, posY - GameConfig.TREE.HEIGHT/2);
            posY -= 150;
        }
    }
}
