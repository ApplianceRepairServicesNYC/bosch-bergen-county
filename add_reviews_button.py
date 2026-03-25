#!/usr/bin/env python3
"""
Add Read Reviews button and modal to all pages.
"""

import os
import re

REVIEWS_BTN_CSS = '''        .reviews-btn {
            background: transparent !important;
            border: 2px solid white !important;
            color: white;
        }
        .reviews-btn:hover {
            background: rgba(255,255,255,0.1) !important;
            transform: translateY(-3px);
        }
        /* Reviews Modal Styles */
        .reviews-modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            z-index: 2000;
            align-items: center;
            justify-content: center;
        }
        .reviews-modal-overlay.active {
            display: flex;
        }
        .reviews-modal {
            background: white;
            border-radius: 12px;
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            position: relative;
        }
        .reviews-modal-header {
            background: linear-gradient(135deg, #003087 0%, #00205B 100%);
            color: white;
            padding: 20px;
            border-radius: 12px 12px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .reviews-modal-header h2 {
            margin: 0;
            font-size: 24px;
        }
        .reviews-modal-close {
            background: none;
            border: none;
            color: white;
            font-size: 28px;
            cursor: pointer;
            padding: 0;
            line-height: 1;
        }
        .reviews-modal-content {
            padding: 25px;
        }
        .review-item {
            border-bottom: 1px solid #eee;
            padding: 20px 0;
        }
        .review-item:last-child {
            border-bottom: none;
        }
        .review-stars {
            color: #ffc107;
            font-size: 18px;
            margin-bottom: 8px;
        }
        .review-text {
            color: #333;
            line-height: 1.6;
            margin-bottom: 8px;
        }
        .review-author {
            color: #666;
            font-size: 14px;
            font-style: italic;
        }
        '''

REVIEWS_MODAL_HTML = '''
    <!-- Reviews Modal -->
    <div class="reviews-modal-overlay" id="reviewsModalOverlay">
        <div class="reviews-modal">
            <div class="reviews-modal-header">
                <h2>Customer Reviews</h2>
                <button class="reviews-modal-close" id="closeReviewsBtn">&times;</button>
            </div>
            <div class="reviews-modal-content">
                <div class="review-item">
                    <div class="review-stars">★★★★★</div>
                    <p class="review-text">"Outstanding service! The technician arrived on time and fixed my Bosch dishwasher the same day. Very professional and knowledgeable. Highly recommend!"</p>
                    <p class="review-author">— Michael R., Ridgewood</p>
                </div>
                <div class="review-item">
                    <div class="review-stars">★★★★★</div>
                    <p class="review-text">"My Bosch refrigerator stopped cooling and they had a technician here within 2 hours. Fixed the issue quickly and the price was very fair. Will definitely use again."</p>
                    <p class="review-author">— Sarah T., Paramus</p>
                </div>
                <div class="review-item">
                    <div class="review-stars">★★★★★</div>
                    <p class="review-text">"Excellent experience from start to finish. The office staff was helpful scheduling and the repair tech knew exactly what was wrong with my Bosch washer. Fixed in under an hour!"</p>
                    <p class="review-author">— David L., Hackensack</p>
                </div>
                <div class="review-item">
                    <div class="review-stars">★★★★★</div>
                    <p class="review-text">"Best appliance repair service in Bergen County. They've fixed my Bosch oven and dryer over the years. Always reliable, always professional. 5 stars!"</p>
                    <p class="review-author">— Jennifer M., Teaneck</p>
                </div>
                <div class="review-item">
                    <div class="review-stars">★★★★★</div>
                    <p class="review-text">"Called in the morning, technician was here by afternoon. He diagnosed the problem with my Bosch cooktop immediately and had it working perfectly. Great service!"</p>
                    <p class="review-author">— Robert K., Fort Lee</p>
                </div>
                <div style="text-align: center; margin-top: 25px; padding: 20px; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 12px;">
                    <p style="color: #fff; font-size: 18px; font-weight: 600; margin-bottom: 5px;">Ready to Book Your Repair?</p>
                    <p style="color: #aaa; font-size: 14px; margin-bottom: 15px;">Same-day service available across Bergen County!</p>
                    <button class="form-call-now" id="reviewsCallBtn" style="margin: 0 auto;">Call Toll-Free</button>
                </div>
            </div>
        </div>
    </div>
'''

REVIEWS_JS = '''
            // Reviews Modal functionality
            var reviewsModalOverlay = document.getElementById('reviewsModalOverlay');
            var openReviewsBtn = document.getElementById('openReviewsBtn');
            var closeReviewsBtn = document.getElementById('closeReviewsBtn');

            if (openReviewsBtn) {
                openReviewsBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    reviewsModalOverlay.classList.add('active');
                    document.body.style.overflow = 'hidden';
                });
            }

            if (closeReviewsBtn) {
                closeReviewsBtn.addEventListener('click', function() {
                    reviewsModalOverlay.classList.remove('active');
                    document.body.style.overflow = '';
                });
            }

            if (reviewsModalOverlay) {
                reviewsModalOverlay.addEventListener('click', function(e) {
                    if (e.target === reviewsModalOverlay) {
                        reviewsModalOverlay.classList.remove('active');
                        document.body.style.overflow = '';
                    }
                });
            }
'''

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Skip if already has reviews button
    if 'reviews-btn' in content and 'reviewsModalOverlay' in content:
        return False

    # 1. Replace hero button with two buttons
    content = re.sub(
        r'<a href="#contact" class="btn">Request Service Today</a>\s*</div>\s*</section>',
        '''<div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
                <a href="#contact" class="btn">Schedule Your Repair</a>
                <button class="btn reviews-btn" id="openReviewsBtn">★ Read Reviews</button>
            </div>
        </div>
    </section>''',
        content
    )

    # 2. Add CSS after .btn:hover if not present
    if '.reviews-btn' not in content:
        content = re.sub(
            r'(\.btn:hover \{[^}]+\})\s*(@media)',
            r'\1\n' + REVIEWS_BTN_CSS + r'\2',
            content
        )

    # 3. Add modal HTML before </footer>
    if 'reviewsModalOverlay' not in content:
        content = content.replace('</footer>\n    <script>', '</footer>\n' + REVIEWS_MODAL_HTML + '\n    <script>')

    # 4. Add JS and setupCallButton for reviewsCallBtn
    if 'reviewsCallBtn' not in content:
        content = re.sub(
            r"(setupCallButton\(document\.getElementById\('ctaCallBtn'\)\);)",
            r"\1\n            setupCallButton(document.getElementById('reviewsCallBtn'));" + REVIEWS_JS,
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
                # Skip index.html since we already updated it manually
                if filepath == os.path.join(base_dir, 'index.html'):
                    continue
                if fix_file(filepath):
                    updated += 1
                    print(f"Updated: {filepath}")

    print(f"\nTotal files updated: {updated}")

if __name__ == '__main__':
    main()
