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
        this.setupInput();
        this.assets = await AssetLoader.loadAssets();
        this.renderer = new Renderer(this.ctx, this.assets);
        this.gameLoop();
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

    setupInput() {
        const handleInteraction = (x) => {
            if (this.gameStatus) {
                const centerX = this.canvas.width / 2;
                this.playerAction(x > centerX ? 1 : 0);
            } else {
                this.startGame();
            }
        }

        this.canvas.addEventListener('touchstart', (event) => {
            event.preventDefault();
            const touch = event.touches[0];
            const rect = this.canvas.getBoundingClientRect();
            handleInteraction(touch.clientX - rect.left);
        })

        this.canvas.addEventListener('click', (event) => {
            const rect = this.canvas.getBoundingClientRect();
            handleInteraction(event.clientX - rect.left);
        })
    }

}