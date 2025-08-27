  // Show welcome loader initially
        setTimeout(() => {
            document.getElementById('welcome-loader').style.display = 'none';
            document.getElementById('dashboard-container').style.display = 'flex';
            
            // Show dashboard by default
            showPage('dashboard');
        }, 2000);

        let isLoggedIn = true; // Set to true for dashboard view
        let currentPage = 'dashboard';

        function showPage(pageId) {
            // Hide all pages
            document.querySelectorAll('.page-content').forEach(page => {
                page.classList.add('hidden');
            });
            
            // Show selected page
            document.getElementById(pageId + '-page').classList.remove('hidden');
            
            // Update page title in header
            const pageTitle = document.getElementById('page-title');
            const pageTitles = {
                'dashboard': 'Dashboard',
                'all-tasks': 'All Tasks',
                'create-task': 'Create Task',
                'edit-task': 'Edit Task',
                'delete-task': 'Delete Task',
                'completed-tasks': 'Completed Tasks',
                'incomplete-tasks': 'Incomplete Tasks',
                'profile': 'Profile',
                'settings': 'Settings'
            };
            pageTitle.textContent = pageTitles[pageId] || 'Dashboard';
            
            // Update active sidebar item
            document.querySelectorAll('.sidebar-item').forEach(item => {
                item.classList.remove('active');
                item.classList.remove('text-white');
                item.classList.add('text-gray-700', 'hover:text-white');
            });
            
            // Find and activate current sidebar item
            const currentSidebarItem = document.querySelector(`[onclick="showPage('${pageId}')"]`);
            if (currentSidebarItem) {
                currentSidebarItem.classList.add('active');
                currentSidebarItem.classList.remove('text-gray-700', 'hover:text-white');
                currentSidebarItem.classList.add('text-white');
            }
            
            currentPage = pageId;
            
            // Close mobile sidebar when page changes
            closeMobileSidebar();
        }

        function logout() {
            isLoggedIn = false;
            // In a real app, you'd redirect to login page or clear session
            showFlashMessage('You have been logged out successfully.', 'info');
            // For demo purposes, just show a message
        }

        function showFlashMessage(message, type = 'info') {
            const flashContainer = document.getElementById('flash-messages');
            const flash = document.createElement('div');
            
            let bgColor = 'bg-blue-500';
            if (type === 'success') bgColor = 'bg-green-500';
            if (type === 'error') bgColor = 'bg-red-500';
            if (type === 'warning') bgColor = 'bg-yellow-500';
            
            flash.className = `${bgColor} text-white px-4 py-3 rounded-lg shadow-lg slide-up max-w-sm`;
            flash.innerHTML = `
                <div class="flex items-center justify-between">
                    <span>${message}</span>
                    <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
            `;
            
            flashContainer.appendChild(flash);
            
            // Auto remove after 5 seconds
            setTimeout(() => {
                if (flash.parentNode) {
                    flash.remove();
                }
            }, 5000);
        }

        // Mobile sidebar toggle
        function toggleMobileSidebar() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('sidebar-overlay');
            
            sidebar.classList.toggle('sidebar-mobile-hidden');
            overlay.classList.toggle('hidden');
        }

        function closeMobileSidebar() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('sidebar-overlay');
            
            sidebar.classList.add('sidebar-mobile-hidden');
            overlay.classList.add('hidden');
        }

        // Event listeners
        document.addEventListener('DOMContentLoaded', function() {
            // Mobile sidebar toggle
            document.getElementById('sidebar-toggle').addEventListener('click', toggleMobileSidebar);
            document.getElementById('sidebar-close').addEventListener('click', closeMobileSidebar);
            document.getElementById('sidebar-overlay').addEventListener('click', closeMobileSidebar);

            // Form submission handlers
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                form.addEventListener('submit', function(e) {
                    e.preventDefault();
                    
                    // Determine action based on current page
                    if (currentPage === 'create-task') {
                        showFlashMessage('Task created successfully!', 'success');
                        showPage('all-tasks');
                    } else if (currentPage === 'edit-task') {
                        showFlashMessage('Task updated successfully!', 'success');
                        showPage('all-tasks');
                    } else if (currentPage === 'profile') {
                        showFlashMessage('Profile updated successfully!', 'success');
                    }
                });
            });

            // Task checkbox handlers
            document.addEventListener('change', function(e) {
                if (e.target.type === 'checkbox' && e.target.closest('.task-card')) {
                    const isChecked = e.target.checked;
                    const taskCard = e.target.closest('.task-card');
                    const taskTitle = taskCard.querySelector('h3');
                    const statusBadge = taskCard.querySelector('span');
                    
                    if (isChecked) {
                        taskTitle.classList.add('line-through');
                        if (statusBadge) {
                            statusBadge.className = 'bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium';
                            statusBadge.textContent = '✅ Completed';
                        }
                        showFlashMessage('Task marked as complete!', 'success');
                    } else {
                        taskTitle.classList.remove('line-through');
                        if (statusBadge) {
                            statusBadge.className = 'bg-orange-100 text-orange-800 px-2 py-1 rounded-full text-xs font-medium';
                            statusBadge.textContent = 'Incomplete';
                        }
                        showFlashMessage('Task marked as incomplete!', 'info');
                    }
                }
            });

            // Search functionality
            const searchInputs = document.querySelectorAll('input[placeholder*="Search"]');
            searchInputs.forEach(input => {
                input.addEventListener('input', function() {
                    // Add your search logic here
                    console.log('Searching for:', this.value);
                });
            });
        });