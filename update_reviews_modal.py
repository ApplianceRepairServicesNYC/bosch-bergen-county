#!/usr/bin/env python3
"""
Update reviews modal to use Elfsight widget like boschappliancerepairnyc.com
"""

import os
import re

# CSS to remove (old custom modal)
OLD_CSS_PATTERNS = [
    r'\.reviews-btn \{[^}]+\}',
    r'\.reviews-btn:hover \{[^}]+\}',
    r'/\* Reviews Modal Styles \*/.*?\.review-author \{[^}]+\}',
    r'\.reviews-modal-overlay[^}]+\}',
    r'\.reviews-modal-overlay\.active[^}]+\}',
    r'\.reviews-modal \{[^}]+\}',
    r'\.reviews-modal-header[^}]+\}',
    r'\.reviews-modal-header h2[^}]+\}',
    r'\.reviews-modal-close[^}]+\}',
    r'\.reviews-modal-content[^}]+\}',
    r'\.review-item[^}]+\}',
    r'\.review-item:last-child[^}]+\}',
    r'\.review-stars[^}]+\}',
    r'\.review-text[^}]+\}',
    r'\.review-author[^}]+\}',
]

# New modal CSS
NEW_MODAL_CSS = '''        /* Reviews Button Style */
        .reviews-btn {
            background: transparent !important;
            border: 2px solid white !important;
            color: white;
        }
        .reviews-btn:hover {
            background: rgba(255,255,255,0.1) !important;
            transform: translateY(-3px);
        }
        /* Modal Styles */
        .modal-overlay {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.7); z-index: 9998; opacity: 0; transition: opacity 0.3s;
        }
        .modal-overlay.active { display: block; opacity: 1; }
        .modal-card {
            display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: white; border-radius: 15px; z-index: 9999; max-width: 700px; width: 90%;
            max-height: 85vh; overflow: hidden; box-shadow: 0 25px 60px rgba(0,0,0,0.4);
        }
        .modal-card.active { display: flex; flex-direction: column; }
        .modal-header {
            background: var(--blue); color: white; padding: 20px 30px;
            display: flex; justify-content: space-between; align-items: center; flex-shrink: 0;
        }
        .modal-header h2 { margin: 0; font-size: 24px; color: white; }
        .modal-close {
            background: rgba(255,255,255,0.2); border: none; color: white; width: 40px; height: 40px;
            border-radius: 50%; font-size: 24px; cursor: pointer; transition: all 0.3s;
        }
        .modal-close:hover { background: var(--red); transform: rotate(90deg); }
        .modal-content { padding: 30px; overflow-y: auto; flex: 1; }
        '''

# New modal HTML
NEW_MODAL_HTML = '''
    <!-- Modal Overlay for Reviews -->
    <div class="modal-overlay" id="modalOverlay"></div>

    <!-- Reviews Modal -->
    <div class="modal-card" id="reviewsModal">
        <div class="modal-header">
            <h2>Customer Reviews</h2>
            <button class="modal-close" data-close="modal">&times;</button>
        </div>
        <div class="modal-content">
            <!-- Elfsight Google Reviews Widget - loaded on demand -->
            <div id="elfsightContainer">
                <div class="elfsight-app-2942fb52-4463-41bc-bc83-d831b9da6f0e"></div>
            </div>
            <div style="text-align: center; margin-top: 25px; padding-top: 20px; border-top: 1px solid #333;">
                <button id="writeReviewBtn" style="background: linear-gradient(45deg, #c41e3a, #a01830); color: white; border: none; padding: 14px 35px; font-size: 16px; font-weight: 600; border-radius: 8px; cursor: pointer; transition: all 0.3s;">Write Your Review</button>
                <p style="margin-top: 12px; color: #666; font-size: 14px;">Had a great experience? Help others by sharing your story!</p>
            </div>
            <div style="text-align: center; margin-top: 25px; padding: 25px; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 12px;">
                <p style="color: #fff; font-size: 18px; font-weight: 600; margin-bottom: 5px;">Ready to Book Your Repair?</p>
                <p style="color: #aaa; font-size: 14px; margin-bottom: 15px;">Same-day service available across Bergen County!</p>
                <button id="reviewsCallBtn" style="background: linear-gradient(45deg, #c41e3a, #a01830); color: white; border: none; padding: 14px 40px; font-size: 16px; font-weight: 600; border-radius: 8px; cursor: pointer; transition: all 0.3s;">📞 Call Toll-Free</button>
            </div>
        </div>
    </div>

    <!-- Write Review Form Modal -->
    <div class="modal-card" id="writeReviewModal" style="max-width: 500px;">
        <div class="modal-header">
            <h2>Write a Review</h2>
            <button class="modal-close" data-close="modal">&times;</button>
        </div>
        <div class="modal-content">
            <form id="reviewForm">
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">Your Name *</label>
                    <input type="text" id="reviewName" required style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; box-sizing: border-box;">
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">Your Rating *</label>
                    <div id="starRating" style="display: flex; gap: 8px; font-size: 32px; cursor: pointer; -webkit-user-select: none; user-select: none;">
                        <span class="star" data-rating="1" tabindex="-1">☆</span>
                        <span class="star" data-rating="2" tabindex="-1">☆</span>
                        <span class="star" data-rating="3" tabindex="-1">☆</span>
                        <span class="star" data-rating="4" tabindex="-1">☆</span>
                        <span class="star" data-rating="5" tabindex="-1">☆</span>
                    </div>
                    <input type="hidden" id="reviewRating" value="0">
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">Your Review *</label>
                    <textarea id="reviewText" required rows="5" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; resize: vertical; box-sizing: border-box;" placeholder="Tell us about your experience..."></textarea>
                </div>
                <button type="submit" style="width: 100%; background: linear-gradient(45deg, #c41e3a, #a01830); color: white; border: none; padding: 14px; font-size: 16px; font-weight: 600; border-radius: 8px; cursor: pointer; transition: all 0.3s;">Submit Review</button>
            </form>
            <div id="reviewThankYou" style="display: none; text-align: center; padding: 40px 20px;">
                <div style="font-size: 60px; margin-bottom: 20px;">✓</div>
                <h3 style="color: #1a1a2e; margin-bottom: 15px;">Thank You for Your Review!</h3>
                <p style="color: #666; font-size: 16px;">Your feedback has been submitted.</p>
            </div>
        </div>
    </div>
'''

# New modal JavaScript
NEW_MODAL_JS = '''
// Lazy load Elfsight widget
var elfsightLoaded = false;
function loadElfsightWidget() {
    if (elfsightLoaded) return;
    var script = document.createElement('script');
    script.src = 'https://static.elfsight.com/platform/platform.js';
    script.defer = true;
    document.body.appendChild(script);
    elfsightLoaded = true;
}

// Modal functionality
var modalOverlay = document.getElementById('modalOverlay');
var reviewsModal = document.getElementById('reviewsModal');
var writeReviewModal = document.getElementById('writeReviewModal');

function openModal(modalId) {
    if (modalOverlay) modalOverlay.classList.add('active');
    var modal = document.getElementById(modalId);
    if (modal) modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeAllModals() {
    if (modalOverlay) modalOverlay.classList.remove('active');
    if (reviewsModal) reviewsModal.classList.remove('active');
    if (writeReviewModal) writeReviewModal.classList.remove('active');
    document.body.style.overflow = '';
}

// Open Reviews Modal button
var openReviewsBtn = document.getElementById('openReviewsBtn');
if (openReviewsBtn) {
    openReviewsBtn.addEventListener('click', function(e) {
        e.preventDefault();
        loadElfsightWidget();
        openModal('reviewsModal');
    });
}

// Write Review Button
var writeReviewBtn = document.getElementById('writeReviewBtn');
if (writeReviewBtn) {
    writeReviewBtn.addEventListener('click', function() {
        if (reviewsModal) reviewsModal.classList.remove('active');
        openModal('writeReviewModal');
    });
}

// Close modal buttons
document.querySelectorAll('.modal-close').forEach(function(btn) {
    btn.addEventListener('click', closeAllModals);
});

// Close on overlay click
if (modalOverlay) {
    modalOverlay.addEventListener('click', closeAllModals);
}

// Close on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeAllModals();
});

// Star Rating functionality
var stars = document.querySelectorAll('#starRating .star');
var ratingInput = document.getElementById('reviewRating');
var currentRating = 0;

stars.forEach(function(star) {
    star.addEventListener('click', function() {
        currentRating = parseInt(this.getAttribute('data-rating'));
        if (ratingInput) ratingInput.value = currentRating;
        updateStars(currentRating);
    });
    star.addEventListener('mouseenter', function() {
        updateStars(parseInt(this.getAttribute('data-rating')));
    });
    star.addEventListener('mouseleave', function() {
        updateStars(currentRating);
    });
});

function updateStars(rating) {
    stars.forEach(function(star, index) {
        star.textContent = index < rating ? '★' : '☆';
        star.style.color = index < rating ? '#ffc107' : '#ccc';
    });
}

// Review Form submission
var reviewForm = document.getElementById('reviewForm');
var reviewThankYou = document.getElementById('reviewThankYou');
if (reviewForm) {
    reviewForm.addEventListener('submit', function(e) {
        e.preventDefault();
        reviewForm.style.display = 'none';
        if (reviewThankYou) reviewThankYou.style.display = 'block';
        setTimeout(function() {
            closeAllModals();
            reviewForm.reset();
            reviewForm.style.display = 'block';
            if (reviewThankYou) reviewThankYou.style.display = 'none';
            currentRating = 0;
            updateStars(0);
        }, 3000);
    });
}
'''

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove old reviews modal HTML
    content = re.sub(
        r'<!-- Reviews Modal -->.*?</div>\s*</div>\s*</div>\s*(?=<script>)',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove old reviews-modal-overlay HTML
    content = re.sub(
        r'<div class="reviews-modal-overlay"[^>]*>.*?</div>\s*</div>\s*</div>\s*(?=<script>)',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove old modal CSS patterns
    content = re.sub(r'/\* Reviews Modal Styles \*/.*?\.review-author \{[^}]+\}\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'\.reviews-modal-overlay \{[^}]+\}\s*', '', content)
    content = re.sub(r'\.reviews-modal-overlay\.active \{[^}]+\}\s*', '', content)
    content = re.sub(r'\.reviews-modal \{[^}]+\}\s*', '', content)
    content = re.sub(r'\.reviews-modal-header \{[^}]+\}\s*', '', content)
    content = re.sub(r'\.reviews-modal-header h2 \{[^}]+\}\s*', '', content)
    content = re.sub(r'\.reviews-modal-close \{[^}]+\}\s*', '', content)
    content = re.sub(r'\.reviews-modal-content \{[^}]+\}\s*', '', content)
    content = re.sub(r'\.review-item \{[^}]+\}\s*', '', content)
    content = re.sub(r'\.review-item:last-child \{[^}]+\}\s*', '', content)
    content = re.sub(r'\.review-stars \{[^}]+\}\s*', '', content)
    content = re.sub(r'\.review-text \{[^}]+\}\s*', '', content)
    content = re.sub(r'\.review-author \{[^}]+\}\s*', '', content)

    # Add new modal CSS after .reviews-btn:hover if not present
    if '.modal-overlay {' not in content:
        content = re.sub(
            r'(\.reviews-btn:hover \{[^}]+\})\s*(@media)',
            r'\1\n' + NEW_MODAL_CSS.replace('.reviews-btn', '.PLACEHOLDER').replace('/* Reviews Button Style */', '/* Modal Styles */') + r'\2',
            content
        )

    # Add new modal HTML before <script>
    if 'id="reviewsModal"' not in content:
        content = re.sub(
            r'(</footer>\s*)(<script>)',
            r'\1' + NEW_MODAL_HTML + r'\n    \2',
            content
        )

    # Remove old reviews modal JavaScript
    content = re.sub(
        r'// Reviews Modal functionality.*?document\.body\.style\.overflow = \'\';\s*\}\s*\}\);\s*\}',
        '',
        content,
        flags=re.DOTALL
    )

    # Add new modal JavaScript before the closing script tag or after setupCallButton calls
    if 'loadElfsightWidget' not in content:
        content = re.sub(
            r"(setupCallButton\(document\.getElementById\('reviewsCallBtn'\)\);)",
            r'\1\n' + NEW_MODAL_JS,
            content
        )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    base_dir = '/Users/globalaffiliate/bosch-bergen-county'
    updated = 0

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)
                if fix_file(filepath):
                    updated += 1
                    print(f"Updated: {filepath}")

    print(f"\nTotal files updated: {updated}")

if __name__ == '__main__':
    main()
