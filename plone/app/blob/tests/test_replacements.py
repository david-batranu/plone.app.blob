from plone.app.blob.tests.base import ReplacementTestCase   # import first!

from unittest import defaultTestLoader
from Products.ATContentTypes.interface.file import IATFile, IFileContent
from Products.ATContentTypes.interface.image import IATImage, IImageContent
from Products.ATContentTypes.content.file import ATFile
from Products.ATContentTypes.content.image import ATImage
from plone.app.blob.interfaces import IATBlobFile, IATBlobImage
from plone.app.blob.migrations import migrateATBlobFiles, migrateATBlobImages
from plone.app.blob.field import BlobField
from plone.app.blob.content import ATBlob
from plone.app.blob.tests.utils import getImage


class FileReplacementTests(ReplacementTestCase):

    def testCreateFileBlob(self):
        foo = self.folder[self.folder.invokeFactory('File', 'foo')]
        foo.update(title="I'm blob", file='plain text')
        # check content item
        self.assertEqual(foo.getPortalTypeName(), 'File')
        self.assertEqual(foo.getContentType(), 'text/plain')
        self.assertEqual(str(foo.getFile()), 'plain text')
        # also make sure we're using blobs
        self.failUnless(isinstance(foo, ATBlob), 'no atblob?')
        self.failUnless(isinstance(foo.getField('file'), BlobField), 'no blob?')
        blob = foo.getFile().getBlob().open('r')
        self.assertEqual(blob.read(), 'plain text')

    def testFileBlobInterfaces(self):
        foo = self.folder[self.folder.invokeFactory('File', 'foo')]
        self.failUnless(IATFile.providedBy(foo), 'no IATFile?')
        self.failUnless(IFileContent.providedBy(foo), 'no IFileContent?')
        self.failUnless(IATBlobFile.providedBy(foo), 'no IATBlobFile?')

    def testFileMigration(self):
        foo = self.folder[self.folder.invokeFactory('ATFile', id='foo',
            title='a file', file='plain text', subject=('foo', 'bar'),
            contributors=('me'))]
        # fake old content from before applying the replacement profile
        foo._setPortalTypeName('File')
        foo.reindexObject(idxs=('portal_type',))
        # check to be migrated content
        self.failUnless(isinstance(foo, ATFile), 'not a file?')
        self.assertEqual(foo.Title(), 'a file')
        self.assertEqual(foo.getContentType(), 'text/plain')
        self.assertEqual(foo.getPortalTypeName(), 'File')
        self.assertEqual(foo.Subject(), ('foo', 'bar'))
        self.assertEqual(foo.Contributors(), ('me',))
        # migrate & check migrated content item
        self.assertEqual(migrateATBlobFiles(self.portal),
            'Migrating /plone/Members/test_user_1_/foo (File -> File)\n')
        foo = self.folder['foo']
        self.failUnless(isinstance(foo, ATBlob), 'not a blob?')
        self.failUnless(isinstance(foo.getField('file'), BlobField), 'no blob?')
        self.assertEqual(foo.Title(), 'a file')
        self.assertEqual(foo.getContentType(), 'text/plain')
        self.assertEqual(foo.getPortalTypeName(), 'File')
        self.assertEqual(foo.Subject(), ('foo', 'bar'))
        self.assertEqual(foo.Contributors(), ('me',))
        blob = foo.getImage().getBlob().open('r')
        self.assertEqual(blob.read(), 'plain text')
        # also make sure the catalog is up to date
        brain = self.portal.portal_catalog(id = 'foo')[0]
        self.assertEqual(foo.UID(), brain.UID)
        self.assertEqual(foo.getObjSize(), brain.getObjSize)


class ImageReplacementTests(ReplacementTestCase):

    def testCreateImageBlob(self):
        gif = getImage()
        foo = self.folder[self.folder.invokeFactory('Image', 'foo')]
        foo.update(title="I'm blob", image=gif)
        # check content item
        self.assertEqual(foo.getPortalTypeName(), 'Image')
        self.assertEqual(foo.getContentType(), 'image/gif')
        self.assertEqual(str(foo.getImage()), gif)
        # also make sure we're using blobs
        self.failUnless(isinstance(foo, ATBlob), 'no atblob?')
        self.failUnless(isinstance(foo.getField('image'), BlobField), 'no blob?')
        blob = foo.getImage().getBlob().open('r')
        self.assertEqual(blob.read(), gif)
        # let's also check the `getSize` and `tag` methods
        self.assertEqual(foo.getSize(), (1, 1))
        self.failUnless('/foo/image"' in foo.tag())

    def testImageBlobInterfaces(self):
        foo = self.folder[self.folder.invokeFactory('Image', 'foo')]
        self.failUnless(IATImage.providedBy(foo), 'no IATImage?')
        self.failUnless(IImageContent.providedBy(foo), 'no IImageContent?')
        self.failUnless(IATBlobImage.providedBy(foo), 'no IATBlobImage?')

    def testImageMigration(self):
        gif = getImage()
        foo = self.folder[self.folder.invokeFactory('ATImage', id='foo',
            title='an image', image=gif, subject=('foo', 'bar'),
            contributors=('me'))]
        # fake old content from before applying the replacement profile
        foo._setPortalTypeName('Image')
        foo.reindexObject(idxs=('portal_type',))
        # check to be migrated content
        self.failUnless(isinstance(foo, ATImage), 'not an image?')
        self.assertEqual(foo.Title(), 'an image')
        self.assertEqual(foo.getContentType(), 'image/gif')
        self.assertEqual(foo.getPortalTypeName(), 'Image')
        self.assertEqual(foo.Subject(), ('foo', 'bar'))
        self.assertEqual(foo.Contributors(), ('me',))
        # migrate & check migrated content item
        self.assertEqual(migrateATBlobImages(self.portal),
            'Migrating /plone/Members/test_user_1_/foo (Image -> Image)\n')
        foo = self.folder['foo']
        self.failUnless(isinstance(foo, ATBlob), 'not a blob?')
        self.failUnless(isinstance(foo.getField('image'), BlobField), 'no blob?')
        self.assertEqual(foo.Title(), 'an image')
        self.assertEqual(foo.getContentType(), 'image/gif')
        self.assertEqual(foo.getPortalTypeName(), 'Image')
        self.assertEqual(foo.Subject(), ('foo', 'bar'))
        self.assertEqual(foo.Contributors(), ('me',))
        blob = foo.getImage().getBlob().open('r')
        self.assertEqual(blob.read(), gif)
        # also make sure the catalog is up to date
        brain = self.portal.portal_catalog(id = 'foo')[0]
        self.assertEqual(foo.UID(), brain.UID)
        self.assertEqual(foo.getObjSize(), brain.getObjSize)


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)

