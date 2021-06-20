function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function foo() {
    await sleep(1000);
    console.log(1);
}

foo();


