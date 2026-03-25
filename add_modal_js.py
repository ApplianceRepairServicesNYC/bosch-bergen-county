#!/usr/bin/env python3
"""
Add missing modal JavaScript to pages that have the modal HTML but missing JS.
"""

import os
import re

MODAL_JS = '''
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

    # Skip if already has the JS
    if 'loadElfsightWidget' in content:
        return False

    # Skip if doesn't have the modal HTML
    if 'id="modalOverlay"' not in content:
        return False

    original = content

    # Find where to insert the JS - after setupCallButton calls or before cfContactForm
    # Try to find setupCallButton(document.getElementById('reviewsCallBtn'));
    if "setupCallButton(document.getElementById('reviewsCallBtn'));" in content:
        content = content.replace(
            "setupCallButton(document.getElementById('reviewsCallBtn'));",
            "setupCallButton(document.getElementById('reviewsCallBtn'));" + MODAL_JS
        )
    elif "setupCallButton(document.getElementById('ctaCallBtn'));" in content:
        content = content.replace(
            "setupCallButton(document.getElementById('ctaCallBtn'));",
            "setupCallButton(document.getElementById('ctaCallBtn'));\n            setupCallButton(document.getElementById('reviewsCallBtn'));" + MODAL_JS
        )
    elif "const cfContactForm = document.getElementById('cfContactForm');" in content:
        content = content.replace(
            "const cfContactForm = document.getElementById('cfContactForm');",
            MODAL_JS + "\n            const cfContactForm = document.getElementById('cfContactForm');"
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
