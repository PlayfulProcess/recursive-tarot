// Hero Spiral Component with Overlaid Text
// Uses the existing spiral with centered text that breathes with the animation
// Based on Greg McKeown's Essential/Effortless + Recursive framework

// Use the existing generateSpiralPath from spiral.js
// We'll just reference it since spiral.js loads first

// Create Hero Spiral with Overlaid Text
function createHeroSpiral(className = '', color = 'currentColor') {
    // Create container div for spiral and text
    const container = document.createElement('div');
    container.className = `hero-spiral-container ${className}`;
    container.style.position = 'relative';
    container.style.display = 'inline-block';
    
    // Create SVG spiral (using existing function)
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 100 100');
    svg.setAttribute('class', 'hero-spiral');
    svg.setAttribute('aria-label', 'Recursive.eco Philosophy - Essential, Effortless, Recursive');
    
    // Create main spiral path (background, more transparent)
    const mainPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    mainPath.setAttribute('d', generateSpiralPath(100, 6, true));
    mainPath.setAttribute('class', 'spiral-path hero-spiral-path-background');
    mainPath.style.stroke = color;
    mainPath.style.strokeWidth = '0.8';
    mainPath.style.fill = 'none';
    mainPath.style.opacity = '0.3';
    
    svg.appendChild(mainPath);
    
    // Create text overlay elements
    const textOverlay = document.createElement('div');
    textOverlay.className = 'hero-text-overlay';
    textOverlay.style.position = 'absolute';
    textOverlay.style.top = '0';
    textOverlay.style.left = '0';
    textOverlay.style.width = '100%';
    textOverlay.style.height = '100%';
    textOverlay.style.display = 'flex';
    textOverlay.style.flexDirection = 'column';
    textOverlay.style.justifyContent = 'center';
    textOverlay.style.alignItems = 'center';
    textOverlay.style.pointerEvents = 'none';
    
    // WHY - Center text (Meaning) - Slowest breathing
    const whyText = document.createElement('div');
    whyText.className = 'hero-text-why';
    whyText.innerHTML = '<span style="font-weight: 600;">WHY:</span> Make sense';
    whyText.style.position = 'absolute';
    whyText.style.fontSize = '28px';
    whyText.style.color = color;
    whyText.style.textAlign = 'center';
    whyText.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif';
    whyText.style.opacity = '0.9';
    
    // HOW - Upper text (Recursive) - Medium breathing
    const howText = document.createElement('div');
    howText.className = 'hero-text-how';
    howText.innerHTML = '<span style="font-weight: 600;">HOW:</span> Recursive';
    howText.style.position = 'absolute';
    howText.style.fontSize = '24px';
    howText.style.color = color;
    howText.style.textAlign = 'center';
    howText.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif';
    howText.style.opacity = '0.8';
    howText.style.top = '25%';
    
    // WHAT - Lower text (Make Belief) - Fastest breathing
    const whatText = document.createElement('div');
    whatText.className = 'hero-text-what';
    whatText.innerHTML = '<span style="font-weight: 600;">WHAT:</span> Make Belief';
    whatText.style.position = 'absolute';
    whatText.style.fontSize = '20px';
    whatText.style.color = color;
    whatText.style.textAlign = 'center';
    whatText.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif';
    whatText.style.opacity = '0.7';
    whatText.style.bottom = '20%';
    
    // Add all text elements to overlay
    textOverlay.appendChild(whyText);
    textOverlay.appendChild(howText);
    textOverlay.appendChild(whatText);
    
    // Add SVG and text overlay to container
    container.appendChild(svg);
    container.appendChild(textOverlay);
    
    return container;
}

// Initialize hero spirals when page loads
function initializeHeroSpirals() {
    // Look for placeholder elements with class 'hero-spiral-placeholder'
    const placeholders = document.querySelectorAll('.hero-spiral-placeholder');
    
    placeholders.forEach(placeholder => {
        // Get color from data attribute or use default
        const color = placeholder.dataset.color || 'currentColor';
        const className = placeholder.className.replace('hero-spiral-placeholder', '').trim();
        
        const heroSpiral = createHeroSpiral(className, color);
        
        // Replace placeholder with hero spiral
        placeholder.parentNode.replaceChild(heroSpiral, placeholder);
    });
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeHeroSpirals);
} else {
    initializeHeroSpirals();
}