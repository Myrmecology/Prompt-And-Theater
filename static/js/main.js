// ============================================================
// PROMPT AND THEATER — Main JavaScript
// ============================================================

const State = {
    sessionId: null,
    playerState: null,
    isLoading: false
}

// ============================================================
// SCREEN MANAGEMENT
// ============================================================

function showScreen(screenId) {
    const screens = ['title-screen', 'loading-screen', 'game-screen', 'gameover-screen']
    screens.forEach(id => {
        const el = document.getElementById(id)
        if (el) el.classList.add('hidden')
    })
    const target = document.getElementById(screenId)
    if (target) target.classList.remove('hidden')
}

// ============================================================
// TRANSITION
// ============================================================

function fadeOut() {
    return new Promise(resolve => {
        const overlay = document.getElementById('transition-overlay')
        overlay.classList.add('fade-in')
        setTimeout(resolve, 400)
    })
}

function fadeIn() {
    return new Promise(resolve => {
        const overlay = document.getElementById('transition-overlay')
        overlay.classList.remove('fade-in')
        setTimeout(resolve, 400)
    })
}

async function transition(callback) {
    await fadeOut()
    await callback()
    await fadeIn()
}

// ============================================================
// NARRATIVE TYPEWRITER EFFECT
// ============================================================

function typeWriter(element, text, speed = 22) {
    return new Promise(resolve => {
        element.textContent = ''
        let i = 0
        const interval = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i)
                i++
            } else {
                clearInterval(interval)
                resolve()
            }
        }, speed)
    })
}

// ============================================================
// UPDATE PLAYER STATS HUD
// ============================================================

function updateStatsHUD(playerState) {
    document.getElementById('health-value').textContent = playerState.health
    document.getElementById('gold-value').textContent = playerState.gold
    document.getElementById('reputation-value').textContent = playerState.reputation

    const actNumerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
    const actIndex = (playerState.act || 1) - 1
    document.getElementById('act-value').textContent = actNumerals[actIndex] || playerState.act

    const healthEl = document.getElementById('stat-health')
    if (playerState.health <= 30) {
        healthEl.style.color = '#CC0000'
    } else if (playerState.health <= 60) {
        healthEl.style.color = '#cc8800'
    } else {
        healthEl.style.color = ''
    }
}

// ============================================================
// RENDER SCENE
// ============================================================

async function renderScene(data) {
    showScreen('game-screen')

    const narrativeEl = document.getElementById('narrative-text')
    const choicesEl = document.getElementById('choices-container')
    const sceneImage = document.getElementById('scene-image')
    const locationBadge = document.getElementById('location-badge')

    // Update location
    if (data.player_state && data.player_state.current_location) {
        locationBadge.textContent = data.player_state.current_location
    }

    // Update stats
    if (data.player_state) {
        updateStatsHUD(data.player_state)
    }

    // Load image
    sceneImage.style.opacity = '0'
    sceneImage.src = data.image_url
    sceneImage.onload = () => {
        sceneImage.style.opacity = '1'
    }
    sceneImage.onerror = () => {
        sceneImage.style.opacity = '0.3'
    }

    // Clear choices while typing
    choicesEl.innerHTML = ''

    // Typewriter narrative
    await typeWriter(narrativeEl, data.narrative)

    // Render choices
    choicesEl.innerHTML = ''
    if (data.choices && data.choices.length > 0) {
        data.choices.forEach(choice => {
            const btn = document.createElement('button')
            btn.className = 'choice-btn'
            btn.textContent = choice
            btn.addEventListener('click', () => handleChoice(choice))
            choicesEl.appendChild(btn)
        })
    }

    State.sessionId = data.session_id
    State.playerState = data.player_state
}

// ============================================================
// START GAME
// ============================================================

async function startGame() {
    if (State.isLoading) return
    State.isLoading = true

    const nameInput = document.getElementById('player-name')
    const playerName = nameInput.value.trim() || 'Stranger'

    await transition(async () => {
        showScreen('loading-screen')
    })

    try {
        const response = await fetch(`/api/game/start?player_name=${encodeURIComponent(playerName)}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        })

        if (!response.ok) throw new Error('Failed to start game')

        const data = await response.json()

        await transition(async () => {
            await renderScene(data)
        })

    } catch (error) {
        console.error('Start game error:', error)
        await transition(async () => {
            showScreen('title-screen')
        })
        alert('The fates are not ready. Please try again.')
    } finally {
        State.isLoading = false
    }
}

// ============================================================
// HANDLE CHOICE
// ============================================================

async function handleChoice(choice) {
    if (State.isLoading || !State.sessionId) return
    State.isLoading = true

    // Disable all choice buttons
    const buttons = document.querySelectorAll('.choice-btn')
    buttons.forEach(btn => {
        btn.disabled = true
        btn.style.opacity = '0.4'
    })

    await transition(async () => {
        showScreen('loading-screen')
    })

    try {
        const response = await fetch('/api/game/choice', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: State.sessionId,
                choice: choice
            })
        })

        if (!response.ok) throw new Error('Failed to process choice')

        const data = await response.json()

        if (data.is_game_over) {
            await transition(async () => {
                showGameOver(data)
            })
        } else {
            await transition(async () => {
                await renderScene(data)
            })
        }

    } catch (error) {
        console.error('Choice error:', error)
        await transition(async () => {
            showScreen('game-screen')
            const buttons = document.querySelectorAll('.choice-btn')
            buttons.forEach(btn => {
                btn.disabled = false
                btn.style.opacity = '1'
            })
        })
    } finally {
        State.isLoading = false
    }
}

// ============================================================
// GAME OVER
// ============================================================

function showGameOver(data) {
    showScreen('gameover-screen')

    const messageEl = document.getElementById('gameover-message')
    const statsEl = document.getElementById('gameover-stats')

    messageEl.textContent = data.game_over_message || 'Your story ends here in Valdermoor.'

    if (data.player_state) {
        const p = data.player_state
        statsEl.innerHTML = `
            <p>Scenes Survived: ${p.scene} &nbsp;|&nbsp; Acts Reached: ${p.act}</p>
            <p style="margin-top:8px">Gold Carried: ${p.gold} &nbsp;|&nbsp; Final Reputation: ${p.reputation}</p>
        `
    }
}

// ============================================================
// RESTART
// ============================================================

async function restartGame() {
    if (State.sessionId) {
        try {
            await fetch(`/api/game/restart/${State.sessionId}`, { method: 'POST' })
        } catch (e) {
            console.error('Restart error:', e)
        }
    }

    State.sessionId = null
    State.playerState = null

    await transition(async () => {
        showScreen('title-screen')
        document.getElementById('player-name').value = ''
    })
}

// ============================================================
// EVENT LISTENERS
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    const beginBtn = document.getElementById('begin-btn')
    const restartBtn = document.getElementById('restart-btn')
    const nameInput = document.getElementById('player-name')

    if (beginBtn) {
        beginBtn.addEventListener('click', startGame)
    }

    if (restartBtn) {
        restartBtn.addEventListener('click', restartGame)
    }

    if (nameInput) {
        nameInput.addEventListener('keydown', e => {
            if (e.key === 'Enter') startGame()
        })
    }
})