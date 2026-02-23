@echo off
echo ========================================
echo  Delete Documentation Files
echo ========================================
echo.
echo This will delete 11 documentation .md files
echo that are NOT used by the application.
echo.
echo Files to be deleted:
echo  1. BEFORE_AFTER_COMPARISON.md
echo  2. CSS_DEBUG_CHECKLIST.md
echo  3. MOBILE_TESTING_GUIDE.md
echo  4. PASSWORD_TOGGLE_FEATURE.md
echo  5. PASSWORD_TOGGLE_SUMMARY.md
echo  6. QUICK_START_RESPONSIVE.md
echo  7. RESPONSIVE_CHANGES_SUMMARY.md
echo  8. RESPONSIVE_DESIGN.md
echo  9. RESPONSIVE_FIX_SUMMARY.md
echo 10. TEST_PASSWORD_TOGGLE.md
echo 11. TEST_RESPONSIVE.md
echo.
echo Files to be KEPT:
echo  - README.md
echo  - SETUP_GUIDE.md
echo.
echo ========================================
echo.
set /p confirm="Are you sure you want to delete these files? (Y/N): "

if /i "%confirm%"=="Y" (
    echo.
    echo Deleting files...
    
    del /F BEFORE_AFTER_COMPARISON.md 2>nul && echo [OK] Deleted BEFORE_AFTER_COMPARISON.md || echo [SKIP] BEFORE_AFTER_COMPARISON.md not found
    del /F CSS_DEBUG_CHECKLIST.md 2>nul && echo [OK] Deleted CSS_DEBUG_CHECKLIST.md || echo [SKIP] CSS_DEBUG_CHECKLIST.md not found
    del /F MOBILE_TESTING_GUIDE.md 2>nul && echo [OK] Deleted MOBILE_TESTING_GUIDE.md || echo [SKIP] MOBILE_TESTING_GUIDE.md not found
    del /F PASSWORD_TOGGLE_FEATURE.md 2>nul && echo [OK] Deleted PASSWORD_TOGGLE_FEATURE.md || echo [SKIP] PASSWORD_TOGGLE_FEATURE.md not found
    del /F PASSWORD_TOGGLE_SUMMARY.md 2>nul && echo [OK] Deleted PASSWORD_TOGGLE_SUMMARY.md || echo [SKIP] PASSWORD_TOGGLE_SUMMARY.md not found
    del /F QUICK_START_RESPONSIVE.md 2>nul && echo [OK] Deleted QUICK_START_RESPONSIVE.md || echo [SKIP] QUICK_START_RESPONSIVE.md not found
    del /F RESPONSIVE_CHANGES_SUMMARY.md 2>nul && echo [OK] Deleted RESPONSIVE_CHANGES_SUMMARY.md || echo [SKIP] RESPONSIVE_CHANGES_SUMMARY.md not found
    del /F RESPONSIVE_DESIGN.md 2>nul && echo [OK] Deleted RESPONSIVE_DESIGN.md || echo [SKIP] RESPONSIVE_DESIGN.md not found
    del /F RESPONSIVE_FIX_SUMMARY.md 2>nul && echo [OK] Deleted RESPONSIVE_FIX_SUMMARY.md || echo [SKIP] RESPONSIVE_FIX_SUMMARY.md not found
    del /F TEST_PASSWORD_TOGGLE.md 2>nul && echo [OK] Deleted TEST_PASSWORD_TOGGLE.md || echo [SKIP] TEST_PASSWORD_TOGGLE.md not found
    del /F TEST_RESPONSIVE.md 2>nul && echo [OK] Deleted TEST_RESPONSIVE.md || echo [SKIP] TEST_RESPONSIVE.md not found
    
    echo.
    echo ========================================
    echo  Deletion Complete!
    echo ========================================
    echo.
    echo Remaining .md files:
    dir *.md /b 2>nul
    echo.
    echo Your application will continue to work normally.
    echo No impact on backend, frontend, or deployment.
    echo.
) else (
    echo.
    echo Deletion cancelled. No files were deleted.
    echo.
)

pause
