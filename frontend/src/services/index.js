import * as authApi from './mocks/auth.js';
import * as clubsApi from './mocks/clubs.js';
import * as eventsApi from './mocks/events.js';
import * as notificationsApi from './mocks/notifications.js';
import * as registrationsApi from './mocks/registrations.js';
import * as attendanceApi from './mocks/attendance.js';
import * as reportsApi from './mocks/reports.js';
import * as recommendationsApi from './mocks/recommendations.js';
import * as statsApi from './mocks/stats.js';
import * as usersApi from './mocks/users.js';

// Central exports for services connected to the backend API.
export const authService = authApi;
export const clubService = clubsApi;
export const eventService = eventsApi;
export const registrationService = registrationsApi;
export const notificationService = notificationsApi;
export const attendanceService = attendanceApi;
export const reportService = reportsApi;
export const recommendationService = recommendationsApi;
export const statsService = statsApi;
export const userService = usersApi;