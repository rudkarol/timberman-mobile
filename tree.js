export class Tree {
    constructor() {
        this.tree = [];
        this.loadArray();
    }

    loadArray() {
        this.tree = [0, 0];
        for (let i = 0; i < 5; i++) {
            this.tree.push(this.generate());
        }
    }

    generate() {
        const rand = Math.random();
        if (rand < 0.5) return 0;
        if (rand < 0.75) return 1;
        return 2;
    }
}
