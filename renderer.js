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

            let segmentWidth
            if (node === 0) {
                segmentWidth = GameConfig.TREE.BASE_WIDTH;
            } else {
                segmentWidth = GameConfig.TREE.BRANCH_WIDTH;
            }
            
            const treeX = this.treeCenterX - (GameConfig.TREE.BASE_WIDTH / 2);

            let xOffset;
            if (node === 0) {
                xOffset = 0;
            } else {
                xOffset = (this.treeBranchWidth - this.treeBaseWidth) / 2;
            }
            
            this.ctx.drawImage(img, treeX - xOffset, posY - GameConfig.TREE.HEIGHT/2);
            posY -= 150;
        }
    }

    drawPlayer(isRightSide, isAnimating) {
        const playerX = isRightSide ? GameConfig.PLAYER.RIGHT_X : GameConfig.PLAYER.LEFT_X;
        const playerImage = isAnimating ? this.assets.player1 : this.assets.player;
        
        this.ctx.save();
        if (!isRightSide) {
            this.ctx.scale(-1, 1);
            this.ctx.drawImage(playerImage, -playerX - 50, GameConfig.PLAYER.Y - 50);
        } else {
            this.ctx.drawImage(playerImage, playerX - 50, GameConfig.PLAYER.Y - 50);
        }
        this.ctx.restore();
    }
}
