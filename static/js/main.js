// ============================================================
// PROMPT AND THEATER — Main JavaScript
// ============================================================

const State = {
    sessionId: null,
    playerState: null,
    isLoading: false,
    currentAct: 1,
    decisionCount: 0
}

// ============================================================
// SCREEN MANAGEMENT
// ============================================================

function showScreen(screenId) {
    const screens = [
        'title-screen',
        'loading-screen',
        'game-screen',
        'gameover-screen',
        'act-transition-screen'
    ]
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
// ACT TRANSITION
// ============================================================

const ACT_SUBTITLES = [
    'A new chapter unfolds in Valdermoor',
    'The darkness deepens across the realm',
    'Blood and shadow consume the land',
    'The final reckoning draws near',
    'Fate cannot be outrun',
    'The world bends to your choices',
    'Legends are forged in suffering',
    'The end begins here',
    'Nothing remains but the truth',
    'Valdermoor remembers everything'
]

const ACT_NUMERALS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']

async function showActTransition(actNumber) {
    const numeral = ACT_NUMERALS[(actNumber - 1)] || String(actNumber)
    const subtitle = ACT_SUBTITLES[(actNumber - 2)] || 'A new chapter unfolds in Valdermoor'

    document.getElementById('act-transition-numeral').textContent = numeral
    document.getElementById('act-transition-subtitle').textContent = subtitle

    await fadeOut()
    showScreen('act-transition-screen')
    await fadeIn()

    await new Promise(resolve => setTimeout(resolve, 2800))

    await fadeOut()
    showScreen('loading-screen')
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
    document.getElementById('scene-value').textContent = playerState.scene

    const actIndex = (playerState.act || 1) - 1
    document.getElementById('act-value').textContent = ACT_NUMERALS[actIndex] || playerState.act

    if (playerState.player_name) {
        document.getElementById('name-value').textContent = playerState.player_name
    }

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
// UPDATE INVENTORY
// ============================================================

function updateInventory(playerState) {
    const inventoryEl = document.getElementById('inventory-list')
    if (!inventoryEl) return

    if (!playerState.inventory || playerState.inventory.length === 0) {
        inventoryEl.innerHTML = '<span class="sidebar-empty">Nothing carried</span>'
        return
    }

    inventoryEl.innerHTML = playerState.inventory.map(item => `
        <div class="inventory-item">${item}</div>
    `).join('')
}

// ============================================================
// UPDATE DECISION LOG
// ============================================================

function updateDecisionLog(choice) {
    const logEl = document.getElementById('decision-log')
    if (!logEl) return

    const emptyEl = logEl.querySelector('.sidebar-empty')
    if (emptyEl) emptyEl.remove()

    State.decisionCount++

    const entry = document.createElement('div')
    entry.className = 'decision-entry'
    entry.innerHTML = `
        <span class="decision-number">${State.decisionCount}.</span>
        <span class="decision-text">${choice.replace(/^\d+\.\s*/, '')}</span>
    `

    logEl.appendChild(entry)
    logEl.scrollTop = logEl.scrollHeight
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

    if (data.player_state && data.player_state.current_location) {
        locationBadge.textContent = data.player_state.current_location
    }

    if (data.player_state) {
        updateStatsHUD(data.player_state)
        updateInventory(data.player_state)
    }

    sceneImage.style.opacity = '0'
    sceneImage.src = data.image_url
    sceneImage.onload = () => {
        sceneImage.style.opacity = '1'
    }
    sceneImage.onerror = () => {
        sceneImage.style.opacity = '0.3'
    }

    choicesEl.innerHTML = ''

    await typeWriter(narrativeEl, data.narrative)

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

    State.currentAct = 1
    State.decisionCount = 0

    const logEl = document.getElementById('decision-log')
    if (logEl) logEl.innerHTML = '<span class="sidebar-empty">No decisions made yet</span>'

    const inventoryEl = document.getElementById('inventory-list')
    if (inventoryEl) inventoryEl.innerHTML = '<span class="sidebar-empty">Nothing carried</span>'

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

    updateDecisionLog(choice)

    const buttons = document.querySelectorAll('.choice-btn')
    buttons.forEach(btn => {
        btn.disabled = true
        btn.style.opacity = '0.4'
    })

    const previousAct = State.playerState ? State.playerState.act : 1

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

        const newAct = data.player_state ? data.player_state.act : 1
        const actAdvanced = newAct > previousAct

        if (data.is_game_over) {
            await transition(async () => {
                showGameOver(data)
            })
        } else if (actAdvanced) {
            State.currentAct = newAct
            await showActTransition(newAct)
            await transition(async () => {
                await renderScene(data)
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
            <p style="margin-top:8px">Decisions Made: ${State.decisionCount}</p>
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
    State.currentAct = 1
    State.decisionCount = 0

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