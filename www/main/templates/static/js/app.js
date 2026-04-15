const API_URL = 'http://localhost:8000/api';
const MEDIA_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', async () => {
    await loadLandingData();
    setupFormHandler();
});

async function loadLandingData() {
    try {
        const response = await fetch(`${API_URL}/landing/`);
        const data = await response.json();

        if (data.hero) {
            document.getElementById('hero-title').textContent = data.hero.title;
            document.getElementById('hero-subtitle').textContent = data.hero.subtitle;
            const heroBtn = document.getElementById('hero-button');
            if (heroBtn) {
                heroBtn.textContent = data.hero.button_text;
                heroBtn.href = data.hero.button_link;
            }
        }

        if (data.statistics) {
            document.getElementById('active-courses').textContent = data.statistics.active_courses;
            document.getElementById('total-students').textContent = data.statistics.total_students;
            document.getElementById('total-teachers').textContent = data.statistics.total_teachers;
            document.getElementById('completed-duels').textContent = data.statistics.completed_duels;
        }

        await loadCourses();
        await loadTestimonials();
        await loadPricing();

        if (data.student_blocks && data.student_blocks.length > 0) {
            renderStudentBlocks(data.student_blocks);
        }

        if (data.teacher_blocks && data.teacher_blocks.length > 0) {
            renderTeacherBlocks(data.teacher_blocks);
        }

        if (data.screenshots) {
            renderScreenshots(data.screenshots);
        }

    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
    }
}

async function loadCourses() {
    try {
        const response = await fetch(`${API_URL}/courses/?is_active=true`);
        const data = await response.json();

        if (data.results) {
            renderCourses(data.results);
        } else if (Array.isArray(data)) {
            renderCourses(data);
        }
    } catch (error) {
        console.error('Ошибка загрузки курсов:', error);
    }
}

async function loadTestimonials() {
    try {
        const response = await fetch(`${API_URL}/testimonials/?is_active=true`);

        if (!response.ok) {
            console.error('Ошибка загрузки отзывов:', response.status);
            return;
        }

        const data = await response.json();
        console.log('Отзывы получены:', data);

        if (data.results) {
            renderTestimonials(data.results);
        } else if (Array.isArray(data)) {
            renderTestimonials(data);
        }
    } catch (error) {
        console.error('Ошибка загрузки отзывов:', error);
    }
}

async function loadPricing() {
    try {
        const response = await fetch(`${API_URL}/pricing/?is_active=true`);
        const data = await response.json();

        if (data.results) {
            renderPricing(data.results);
        } else if (Array.isArray(data)) {
            renderPricing(data);
        }
    } catch (error) {
        console.error('Ошибка загрузки тарифов:', error);
    }
}

function renderStudentBlocks(blocks) {
    const container = document.getElementById('student-blocks');
    if (!container) return;

    container.innerHTML = blocks.map(block => {
        const imagePath = block.icon || '';
        const imageUrl = imagePath ? `${MEDIA_URL}${imagePath}` : '';

        return `
            <div class="card">
                <div class="card-icon">
                    ${imageUrl ? 
                        `<img src="${imageUrl}" alt="${block.title}" style="width:30px; height:30px; object-fit: contain;" onerror="this.style.display='none'; this.nextElementSibling.style.display='inline';">` : 
                        '📚'
                    }
                    <h3 class="card-title">${block.title}</h3>
                </div>
                <p class="card-description">${block.description}</p>
            </div>
        `;
    }).join('');
}

function renderTeacherBlocks(blocks) {
    const container = document.getElementById('teacher-blocks');
    if (!container) return;

    container.innerHTML = blocks.map(block => {
        const imagePath = block.icon || '';
        const imageUrl = imagePath ? `${MEDIA_URL}${imagePath}` : '';

        return `
            <div class="card teacher-card">
                <div class="card-icon">
                    ${imageUrl ? 
                        `<img src="${imageUrl}" alt="${block.title}" style="width:30px; height:30px; object-fit: contain;" onerror="this.style.display='none';">` : 
                        '👩‍🏫'
                    }
                    <h3 class="card-title">${block.title}</h3>
                </div>
                
                <p class="card-description">${block.description}</p>
                
                <div class="teacher-card-footer">
                    <span></span>
                    ${block.feature_link ? 
                        `<a href="${block.feature_link}" class="teacher-card-button">
                            Подробнее 
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M5 12h14"></path>
                                <path d="m12 5 7 7-7 7"></path>
                            </svg>
                        </a>` : 
                        ''
                    }
                </div>
            </div>
        `;
    }).join('');
}

function renderRatingStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

    let starsHtml = '';

    for (let i = 0; i < fullStars; i++) {
        starsHtml += `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="star star-full" fill-opacity="1">
                <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path>
            </svg>
        `;
    }

    if (hasHalfStar) {
        starsHtml += `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="star star-half" fill-opacity="0.5">
                <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path>
            </svg>
        `;
    }

    for (let i = 0; i < emptyStars; i++) {
        starsHtml += `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="star star-empty" fill-opacity="0">
                <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path>
            </svg>
        `;
    }

    return starsHtml;
}

function renderCourses(courses) {
    const container = document.getElementById('courses-grid');
    if (!container) return;

    container.innerHTML = courses.map(course => {
        let imageHtml = '';
        if (course.cover_image) {
            let imageUrl = course.cover_image;
            if (imageUrl.startsWith('/media/')) {
                imageUrl = `http://localhost:8000${imageUrl}`;
            }
            imageHtml = `<img class="course-cover" src="${imageUrl}" alt="${course.title}">`;
        } else {
            imageHtml = `<div class="course-cover-placeholder">📚</div>`;
        }

        const authorName = course.author_name || course.author_detail?.name || 'Кит Макс';

        const description = course.short_description ||
                           (course.description ? course.description.substring(0, 150) : 'Описание курса');

        const studentsCount = course.total_students || 0;
        const formattedStudents = studentsCount >= 1000 ? (studentsCount / 1000).toFixed(1) + 'k' : studentsCount;

        const rating = course.average_rating || 0;
        const roundedRating = rating.toFixed(1);

        const starsHtml = renderRatingStars(rating);

        return `
            <div class="course-card" onclick="showCourseInterest(${course.id})">
                <div class="course-header">
                    <h3>${course.title}</h3>
                    ${imageHtml}
                </div>
                
               
                <p class="course-description">${description}</p>
                
                <div class="course-meta">
                    <span class="course-students">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-graduation-cap text-primary-DEFAULT transition-colors duration-300 group-hover:text-white" aria-hidden="true"><path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"></path><path d="M22 10v6"></path><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"></path></svg> ${formattedStudents} студентов
                    </span>
                    <span class="course-rating">
                        <span class="course-rating-stars">${starsHtml}</span>
                        ${roundedRating}
                    </span>
                </div>
                
                <div class="course-footer">
                    <span class="course-author">Автор: ${authorName}</span>
                    <span class="course-button">
                        К курсу 
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M5 12h14"></path>
                            <path d="m12 5 7 7-7 7"></path>
                        </svg>
                    </span>
                </div>
            </div>
        `;
    }).join('');
}
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}



function renderTestimonials(testimonials) {
    const container = document.getElementById('testimonials-grid');
    if (!container) return;

    container.innerHTML = testimonials.map(testimonial => {
        const starsHtml = renderRatingStars(testimonial.rating);

        return `
            <div class="testimonial-card">
                <div class="testimonial-author">
                    <div class="testimonial-avatar">
                        ${testimonial.display_name?.charAt(0) || 'А'}
                    </div>
                    <div>
                        <div class="testimonial-name">${testimonial.display_name}</div>
                        <div class="testimonial-role">${testimonial.course_title || 'Студент'}</div>
                    </div>
                </div>
                
                <p class="testimonial-text">${testimonial.content}</p>
                
                <div class="testimonial-rating">
                    ${starsHtml}
                </div>
            </div>
        `;
    }).join('');
}
function renderPricing(plans) {
    const container = document.getElementById('pricing-grid');
    if (!container) return;

    container.innerHTML = plans.map(plan => {
        const svgCheck = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 8px; flex-shrink: 0;"><path d="M20 6L9 17L4 12" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

        return `
            <div class="pricing-card ${plan.is_popular ? 'popular' : ''}">
                ${plan.is_popular ? '<div class="popular-badge">Популярный</div>' : ''}
                <h3 class="pricing-name">${plan.name}</h3>
                <div class="pricing-price">
                    <span class="price-amount">${plan.price} ₽</span>
                    <span class="price-period">/${plan.price_period}</span>
                </div>
                <ul class="pricing-features">
                    ${plan.features.map(feature => `<li>${svgCheck} ${feature}</li>`).join('')}
                </ul>
                <button class="btn-pricing" onclick="selectPlan('${plan.name}')">Выбрать</button>
            </div>
        `;
    }).join('');
}

document.addEventListener('DOMContentLoaded', function() {
    const selects = document.querySelectorAll('.select-wrapper select');

    selects.forEach(select => {
        select.addEventListener('click', function() {
            const wrapper = this.closest('.select-wrapper');
            wrapper.classList.toggle('open');
        });

        select.addEventListener('blur', function() {
            const wrapper = this.closest('.select-wrapper');
            wrapper.classList.remove('open');
        });
    });
});
function renderScreenshots(screenshots) {
    const container = document.getElementById('screenshots-grid');
    if (!container) return;

    const allScreenshots = [...(screenshots.student || []), ...(screenshots.teacher || [])];

    container.innerHTML = allScreenshots.map(screenshot => {
        const imagePath = screenshot.image || '';
        const imageUrl = imagePath ? `${MEDIA_URL}${imagePath}` : '';

        return `
            <div class="screenshot-card">
                <div class="screenshot-image">
                    ${imageUrl ? `<img src="${imageUrl}" alt="${screenshot.title}" style="width:100%; height:100%; object-fit:cover;">` : '📸'}
                </div>
                <div class="screenshot-title">${screenshot.title}</div>
            </div>
        `;
    }).join('');
}

function setupFormHandler() {
    const form = document.getElementById('lead-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            user_type: document.getElementById('user_type').value,
            message: document.getElementById('message').value
        };

        const messageDiv = document.getElementById('form-message');
        messageDiv.textContent = 'Отправка...';
        messageDiv.className = 'form-message';

        try {
            const response = await fetch(`${API_URL}/leads/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                messageDiv.textContent = data.message || 'Заявка успешно отправлена! Мы свяжемся с вами.';
                messageDiv.className = 'form-message success';
                form.reset();
            } else {
                const errors = Object.values(data).flat().join(', ');
                messageDiv.textContent = `Ошибка: ${errors || 'Проверьте введенные данные'}`;
                messageDiv.className = 'form-message error';
            }
        } catch (error) {
            messageDiv.textContent = 'Ошибка соединения. Попробуйте позже.';
            messageDiv.className = 'form-message error';
            console.error('Ошибка отправки:', error);
        }
    });
}

function selectPlan(planName) {
    const messageDiv = document.getElementById('form-message');
    if (messageDiv) {
        messageDiv.textContent = `Вы выбрали тариф "${planName}". Заполните форму ниже для оформления.`;
        messageDiv.className = 'form-message success';
        document.getElementById('register').scrollIntoView({ behavior: 'smooth' });
    }
}

function showCourseInterest(courseId) {
    const messageDiv = document.getElementById('form-message');
    if (messageDiv) {
        messageDiv.textContent = `Вы выбрали курс. Заполните форму ниже для записи.`;
        messageDiv.className = 'form-message success';
        document.getElementById('register').scrollIntoView({ behavior: 'smooth' });
    }
}

const mobileBtn = document.getElementById('mobileMenuBtn');
const navLinks = document.querySelector('.nav-links');

if (mobileBtn) {
    mobileBtn.addEventListener('click', () => {
        mobileBtn.classList.toggle('active');
        navLinks.classList.toggle('active');
    });
}