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
}