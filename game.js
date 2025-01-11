import { Tree } from "./tree.js";
import { AssetLoader } from "./assetLoader.js";
import { Renderer } from "./renderer.js";
import { GameConfig } from "./config.js";

export class Game {
    constructor() {
        this.canvas = document.getElementById("gameCanvas");
        this.ctx = this.canvas.getContext("2d");
        this.tree = new Tree();
        this.currentPosition = true;
        this.gameStatus = false;
        this.points = 0;
        this.playerAnimationStatus = false;
        this.scale = 1;
        
        this.init();
    }

    async init() {
        this.assets = await AssetLoader.loadAssets();
        this.renderer = new Renderer(this.ctx, this.assets);
    }

    startGame() {
        this.tree.loadArray();
        this.points = 0;
        this.gameStatus = true;
    }

    draw() {
        this.ctx.setTransform(1, 0, 0, 1, 0, 0);
        this.ctx.scale(this.scale, this.scale);
        
        this.renderer.clearScreen();
        this.renderer.drawBackground();
        this.renderer.drawUI(this.points, this.gameStatus);
        this.renderer.drawTree(this.tree);
        this.renderer.drawPlayer(this.currentPosition, this.playerAnimationStatus);
    }

    gameLoop() {
        this.draw();
        requestAnimationFrame(() => this.gameLoop());
    }

    playerAction(position) {
        if (position !== -1) {
            this.currentPosition = Boolean(position);
            this.playerAnimationStatus = true;
            setTimeout(() => {this.playerAnimationStatus = false}, 40);
            this.cutTree();
        }
    }

    cutTree() {
        const treeStatus = this.tree.getAndGenerate();

        if ((treeStatus === 1 && !this.currentPosition) || 
            (treeStatus === 2 && this.currentPosition)) {
            this.gameStatus = false;
            this.lastGameEndTime = Date.now();
        } else {
            this.points++;
        }
    }

}